import redis
from scrapy.utils.serialize import ScrapyJSONEncoder

class RedisUtil(object):

	server = redis.Redis()
	encoder = ScrapyJSONEncoder()

	@classmethod
	def set(self, key, value):
		try:
			self.server.set(key, value)
		except:
			return False

	@classmethod
	def get(self, key):
		try:
			return self.server.get(key)
		except:
			return None