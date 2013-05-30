#!/usr/bin/env python
# coding: utf-8

import web
from config import settings

db = settings.db
table_article = 'article'
render = settings.render

class Index:
	def GET(self):
		articles = db.select(table_article, where="status=1", order="published_time desc", limit="10" )
		return render.render('index', articles=articles)
