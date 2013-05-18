#!/usr/bin/env python
# coding: utf-8

from config import settings
from util.jsonUtil import getJson
import simplejson
import web

db = settings.db
table = 'sports_video'
render_layout = settings.render_layout


class Video:
	def GET(self, sport_type):
		sport_id = getSportId(sport_type)

		params = web.input()
		page = params.page if hasattr(params, 'page') else 1
		
		per_page = 20
		offset = (int(page) - 1) * per_page
		videos = db.select(table, where='sport_id=%d' % sport_id, order='round desc, gmt_create desc', offset=offset, limit=per_page)
		video_count = db.query("SELECT COUNT(1) AS count FROM %s where sport_id=%d" % (table, sport_id) )[0]
		
		if video_count.count % per_page != 0:
			pages = 1 + video_count.count / per_page
		else:
			pages = video_count.count / per_page

		return render_layout.video(videos, pages)

		# Json返回
		#web.header('Content-Type', 'application/json') 
		#return getJson(videos=videos, totalResultsCount=100)


def getSportId(sport_type):
	sport_id = 0
	if sport_type:
		if sport_type == 'xijia':
			sport_id = 2
		elif sport_type == 'yingchao':
			sport_id = 3
		elif sport_type == 'yijia':
			sport_id = 4
		else:
			sport_id = 5

	return sport_id