# Scrapy settings for sports project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'sports'

SPIDER_MODULES = ['sports.spiders']
NEWSPIDER_MODULE = 'sports.spiders'

ITEM_PIPELINES = ['sports.pipelines.VideoPipeline']

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'sports.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = False


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sports (+http://www.yourdomain.com)'
