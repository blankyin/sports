#!/usr/bin/env python
# coding: utf-8

import web
from config import settings
from pymongo import ASCENDING, DESCENDING

db = settings.db
table_article = 'article'
render = settings.render

class Index:
	def GET(self):
		# mysql
		# articles = db.select(table_article, where="status=1", order="published_time desc", limit="10" )

		# mongodb
		articles = db[table_article].find({'status' : 1}).limit(10).sort('published_time', DESCENDING)
		return render.render('index', articles=articles)
