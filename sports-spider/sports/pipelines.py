#-*-coding:utf-8-*-

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from pymongo import MongoClient
import datetime


class VideoPipelineForMongoDB(object):
	"""
	使用mongodb保存视频相关信息
	"""

	MONGODB_SERVER = "localhost"
	MONGODB_PORT = 27017
	MONGODB_DB = "sports"
	
	def __init__(self):
		try:
			client = MongoClient(self.MONGODB_SERVER, self.MONGODB_PORT)
			self.db = client[self.MONGODB_DB]
		except Exception as e:
			log.msg("connection mongodb error: %s" % str(e), level=log.DEBUG)

	def process_item(self, item, spider):
		sports_video = {
			'sport_id' : item['sport_id'],
			'round' : item['s_round'],
			'title' : item['title'],
			'url' : item['url'],
			'image' : item['image'],
			'time' : item['time'],
			'gmt_create' : datetime.datetime.now()
		}

		count = self.db['sports_video'].find({'url': item['url']}).count()
		if count:
			log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
		else:
			result = self.db['sports_video'].insert(sports_video)
			# result = self.db.runCommand({
			# 	findAndModify : "sports_video",
			# 	query : {"url" : item['url']},
			# 	update : {"$set" : sports_video},
			# 	upsert : True,
			# 	'new' : True
			# })

		return item



class VideoPipelineForMySQL(object):
	"""
	使用mysql保存视频相关信息
	"""
	
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			host="127.0.0.1",
			db = 'spider',
			user = 'root',
			passwd = 'root',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = True
		)

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self.insert_item, item)
		query.addErrback(self.handle_error)
		return item

	def insert_item(self, tx, item):
		tx.execute("select * from sports_video where url=%s", (item['url']))
		result = tx.fetchone()
		if result:
			log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
		else:
			tx.execute("""insert into sports_video(sport_id, round, title, url, image, time, gmt_create) 
	    		values (%s, %s, %s, %s, %s, %s, %s)""", \
	    		(item['sport_id'], item['s_round'], item['title'], item['url'], item['image'], item['time'], datetime.datetime.now())
			)

	def handle_error(self, e):
		log.err(e)