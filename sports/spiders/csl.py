#-*-coding:utf-8-*-

from scrapy import log
#from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule  
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from urlparse import urljoin
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 

from sports.items import CslItem
from sports.utils.select_util import list_first_item, list_last_item
from sports.utils.re_util import get_round
from sports.utils.redis_util import RedisUtil


class CslSpider(CrawlSpider):
	# laliga
	name = "zhongchao"
	allowed_domain = ['sina.com.cn']
	start_urls = ['http://sports.sina.com.cn/video/c/j/csl/']

	s_round = 0;	# 赛事轮次
	video_domain = 'http://sports.sina.com.cn'
	is_over = False

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		
		# 初始化最近赛事轮次
		if self.s_round == 0 and not self.is_over:	
			pre_last_url = "/html/body/div[@class='wrap']/div[@class='part04']/div[@class='p04_c clearfix']/ul/li[1]/a[@class='p_a alphaImg']/@href"
			pre_last = list_last_item(hxs.select(pre_last_url).extract())
			pre_last = urljoin(self.video_domain, pre_last)
			self.s_round = get_round('http://sports.sina.com.cn/video/c/j/csl/2013_(\w+)/index.shtml', pre_last)

		if self.s_round >= 0:
			if self.s_round > 0:
				if self.s_round == 1:
					next_link = 'http://sports.sina.com.cn/video/c/j/csl/2013_%02d/index.shtml' % self.s_round
				else:
					next_link = 'http://sports.sina.com.cn/video/c/j/csl/2013_%d/index.shtml' % self.s_round
		
				if not RedisUtil.get(next_link):
					next_link = urljoin(self.video_domain, next_link)
					yield Request(url=next_link, callback=self.parse)
					# 使用redis保存已经爬取过的URL，避免重复爬行
					RedisUtil.set(next_link, next_link)
					

			sites = hxs.select("/html/body/div[@class='wrap']/div[@class='part01 clearfix']/div[@class='p01_focus']/div[@id='p01_cont01']/div[@class='p01_video_li']/div[@id='p01_video_cont']/ul[@id='p01_video_cont00']/li")
			items = []
			for site in sites:
				item = CslItem()
				item['sport_id'] = 5 # 中超
				item['s_round'] = self.s_round + 1
				item['title'] = list_first_item(site.select("h2/span/a/text()").extract())
				item['url'] = list_first_item(site.select("h2/a[@class='a_more']/@href").extract())
				item['image'] = list_first_item(site.select("div/blockquote[1]/a[@class='v_a btn_video']/img/@src").extract())
				item['time'] = list_first_item(site.select("div/blockquote[1]/a[@class='v_a btn_video']/s/text()").extract()).rstrip('"')
				yield item

			self.s_round -= 1
			if self.s_round == 0:
				self.is_over = True;