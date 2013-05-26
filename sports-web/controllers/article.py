#!/usr/bin/env python
# coding: utf-8

import web
from config import settings
from controllers.utils import login_required
from util.jsonUtil import getJson

db = settings.db
table_article = 'article'
table_category = 'category'
table_article_category = 'article_category'
table_article_tag = 'article_tag'
render = settings.render

class Article:
	def GET(self):
		"""
		文章页面
		"""
		data = web.input()
		page = data.page if hasattr(data, 'page') else 1
		per_page = 10
		offset = (int(page) - 1) * per_page

		articles = list(db.select(table_article, where="status=1", order="published_time desc", offset=offset, limit=per_page))
		article_count = db.query("SELECT COUNT(1) as count FROM %s where status=1" % table_article)[0]	

		if article_count.count % per_page != 0:
			pages = 1 + article_count.count / per_page
		else:
			pages = article_count.count / per_page

		return render.render('article/article', articles=articles, pages=pages, page=page)


class ArticleDetail:
	def GET(self):
		data = web.input()
		article_id = data.get('article_id', '')
		articles = db.select(table_article, where="id=%s" % article_id)
		if articles:
			article = articles[0]

		return render.render('article/article_detail', article=article)


class DelArticle:
	@login_required
	def POST(self):
		"""
		删除文章
		"""
		data = web.input()
		article_id = data.get('article_id', '')
		if article_id:
			username = web.ctx.session.username
			update_count = db.update(table_article, where='id=%s' % article_id, status=-1, modify_name=username, gmt_modify=web.SQLLiteral('now()'))
		if update_count > 0:
			result = 'true'
		else:
			result = 'false'

		json = getJson(msg=result)
		return json


class AddArticle:
	@login_required
	def GET(self):
		"""
		发表文章页面
		"""
		return render.render('article/add_article', categorys=get_categorys())

	@login_required
	def POST(self):
		"""
		新增文章（事务）
		"""
		data = web.input(categorys=[])
		article_title = data.get('article_title', '')
		article_content = data.get('article_content', '')
		tags = data.get('tags', '')
		categorys = data.get('categorys', '')

		if not article_title or not article_content:
			return web.seeother('/article/add_article')
		
		t = db.transaction()
		try:
			article_id = db.insert(table_article, article_title=article_title, article_content=article_content, 
									status=1, published_time=web.SQLLiteral('now()'), published_name=web.ctx.session.username)
			if article_id:
				self.add_tags(article_id, tags)
				self.add_article_category(article_id, categorys)
		except:
			t.rollback()
		else:
			t.commit()
		return web.seeother('/article/article')

	@login_required
	def add_tags(self, article_id, tags):
		"""
		新增标签
		"""
		if tags:
			t = db.transaction()
			try:
				for tag in tags.split(','):
					db.insert(table_article_tag, article_id=article_id, tag=tag, status=1, 
								gmt_create=web.SQLLiteral('now()'), create_name=web.ctx.session.username)
			except:
				t.rollback()
			else:
				t.commit()

	@login_required
	def add_article_category(self, article_id, categorys):
		"""
		新增文章类目关系
		"""
		if categorys:
			t = db.transaction()
			try:
				for category_id in categorys:
					db.insert(table_article_category, article_id=article_id, category_id=category_id, status=1,
								gmt_create=web.SQLLiteral('now()'), create_name=web.ctx.session.username)
			except:
				t.rollback()
			else:
				t.commit()


class EditArticle:
	@login_required
	def GET(self):
		"""
		发表文章页面
		"""
		data = web.input()
		article_id = data.get('article_id', '')
		if article_id:
			article = db.select(table_article, where="id=%s" % article_id)[0]
			tags = db.query("select group_concat(tag) as tags from article_tag where status=1 and article_id=%s" % article_id)[0]
			select_categorys = db.query("select category_id from article_category where status=1 and article_id=%s" % article_id)
		else:
			# 404
			pass
		if not tags.tags:
			tags.tags = ''

		select_categorys = list(( category.category_id for category in select_categorys))
		return render.render('article/edit_article', article=article, tags=tags.tags, select_categorys=select_categorys, categorys=get_categorys())

	@login_required
	def POST(self):
		"""
		更新文章（事务）
		"""
		data = web.input(categorys=[])
		article_id = data.get('article_id', 0)
		article_title = data.get('article_title', '')
		article_content = data.get('article_content', '')
		tags = data.get('tags', '')
		categorys = data.get('categorys', '')

		if not article_title or not article_content:
			return web.seeother('/article/add_article')
		
		t = db.transaction()
		try:
			update_count = db.update(table_article, where="id=%s" % article_id, article_title=article_title, article_content=article_content, 
									status=1, gmt_modify=web.SQLLiteral('now()'), modify_name=web.ctx.session.username)
			if update_count:
				self.update_tags(article_id, tags)
				self.update_article_category(article_id, categorys)
		except:
			t.rollback()
		else:
			t.commit()
		return  web.seeother('/article/article')

	@login_required
	def update_tags(self, article_id, tags):
		"""
		新增标签
		"""
		if tags:
			t = db.transaction()
			try:
				# 先将原来的标签状态置为无效
				db.update(table_article_tag, where="article_id=%s" % article_id, status=-1)

				for tag in tags.split(','):
					results = db.select(table_article_tag, where="article_id=%s and tag='%s'" % (article_id, tag))
					if results:
						db.update(table_article_tag, where="article_id=%s and tag='%s'" % (article_id, tag), status=1)
					else:
						db.insert(table_article_tag, article_id=article_id, tag=tag, status=1, 
								gmt_create=web.SQLLiteral('now()'), create_name=web.ctx.session.username)	
			except:
				t.rollback()
			else:
				t.commit()

	@login_required
	def update_article_category(self, article_id, categorys):
		"""
		新增文章类目关系
		"""
		if categorys:
			t = db.transaction()
			try:
				# 先将原来的分类状态置为无效
				db.update(table_article_category, where="article_id=%s" % article_id, status=-1)

				for category_id in categorys:
					results = db.select(table_article_category, where="article_id=%s and category_id=%s" % (article_id, category_id))
					if results:
						db.update(table_article_category, where="article_id=%s and category_id=%s" % (article_id, category_id), status=1)
					else:
						db.insert(table_article_category, article_id=article_id, category_id=category_id, status=1,
								gmt_create=web.SQLLiteral('now()'), create_name=web.ctx.session.username)	
			except:
				t.rollback()
			else:
				t.commit()


class Category:
	@login_required
	def GET(self):
		return render.render('article/category', categorys=get_categorys())

	@login_required
	def POST(self):
		"""
		新增文章分类
		"""
		data = web.input()
		category_name = data.get('category_name', '')
		if category_name and len(category_name.strip(' ')) > 0:
			username = web.ctx.session.username
			db.insert(table_category, name=category_name, status=1, create_name=username, gmt_create=web.SQLLiteral('now()'))
		return web.seeother('/article/category')


class DelCategory:
	"""
	删除文章分类
	"""
	@login_required
	def POST(self):
		data = web.input()
		category_id = data.get('category_id', 0)
		if category_id:
			username = web.ctx.session.username
			update_count = db.update(table_category, where='id=%s' % category_id, status=-1, modify_name=username, gmt_modify=web.SQLLiteral('now()'))
		if update_count > 0:
			result = 'true'
		else:
			result = 'false'

		json = getJson(msg=result)
		return json


def get_categorys():
	categorys = list(db.query(""" 
			select 
					cat.id,
					cat.name, 
					cat.gmt_create,
					(select count(1) from article_category ac where ac.status=1 and ac.category_id = cat.id) article_num
		  	  from category cat
		  	 where cat.status = 1 
		  	 order by gmt_create
		"""))
	return categorys