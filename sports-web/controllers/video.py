#!/usr/bin/env python
# coding: utf-8

from config import settings

db = settings.db
table = 'sports_video'
render = settings.render

class Index:
	def GET(self):
		videos = db.select(table, order='gmt_create desc')
		return render.index(videos)