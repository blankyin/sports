#-*-coding:utf-8-*-

BOT_NAME = 'sports'

SPIDER_MODULES = ['sports.spiders']
NEWSPIDER_MODULE = 'sports.spiders'

#SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = [
	'sports.pipelines.VideoPipeline',
	#'scrapy_redis.pipelines.RedisPipeline'
]

# 禁用cookie
COOKIES_ENABLED = False

# 下载延迟
DOWNLOAD_DELAY = 2

GOOGLE_CACHE_DOMAINS = ['v.qq.com',]

#To make ChangeUserAgentMiddleware enable.
USER_AGENT = ''

DOWNLOADER_MIDDLEWARES = {
	# 使用GoogleCacheMiddleware时可能出现的问题：1. XPath可能不同；2. 部分缓存页面不存在
	#'sports.contrib.downloadmiddleware.google_cache.GoogleCacheMiddleware':500,
	#'sports.contrib.downloadmiddleware.proxy.ProxyMiddleware':50,
    'sports.contrib.downloadmiddleware.change_useragent.ChangeUserAgentMiddleware':500,
}

COMMANDS_MODULE = 'sports.commands'

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'sports.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sports (+http://www.yourdomain.com)'
