#!/usr/bin/env python
# coding: utf-8

from config import settings
from util.jsonUtil import getJson
import simplejson
import web
from pymongo import ASCENDING, DESCENDING

db = settings.db
table = 'sports_video'
render = settings.render


class Video:
	def GET(self, sport_type):
		sport_id, sport_name = getSportId(sport_type)

		params = web.input()
		page = params.page if hasattr(params, 'page') else 1
		
		per_page = 10
		offset = (int(page) - 1) * per_page

		# mysql
		# videos = db.select(table, where='sport_id=%d' % sport_id, order='round desc, gmt_create desc', offset=offset, limit=per_page)
		# video_count = db.query("SELECT COUNT(1) AS count FROM %s where sport_id=%d" % (table, sport_id) )[0].count

		# mongodb
		videos = db[table].find({'sport_id' : sport_id}).limit(per_page).skip(offset).sort([('round', DESCENDING), ('gmt_create', DESCENDING)])
		video_count = videos.count()

		if video_count % per_page != 0:
			pages = 1 + video_count / per_page
		else:
			pages = video_count / per_page

		data = {}
		data['sport_name'] = sport_name
		data['videos'] = videos
		data['pages'] = pages
		data['page'] = page
		return render.video(data)

		# Json返回
		#web.header('Content-Type', 'application/json') 
		#return getJson(videos=videos, totalResultsCount=100)


def getSportId(sport_type):
	sport_id = 0
	sport_name = u''
	if sport_type:
		if sport_type == u'xijia':
			sport_id = 2
			sport_name = u'西甲'
		elif sport_type == 'yingchao':
			sport_id = 3
			sport_name = u'英超'
		elif sport_type == 'yijia':
			sport_id = 4
			sport_name = u'意甲'
		elif sport_type == 'zhongchao':
			sport_id = 5
			sport_name = u'中超'

	return (sport_id, sport_name)