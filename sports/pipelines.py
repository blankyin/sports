#-*-coding:utf-8-*-

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
import MySQLdb
import MySQLdb.cursors
import datetime

class VideoPipeline(object):
	
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