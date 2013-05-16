#-*-coding:utf-8-*-

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider, Rule  
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from urlparse import urljoin
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor 

from sports.items import PremierleagueItem
from sports.utils.select_util import list_first_item, list_last_item
from sports.utils.re_util import get_round
from sports.utils.redis_util import RedisUtil

class PremierleagueSpider(CrawlSpider):
	# premierleague
	name = "yingchao"
	allowed_domain = ['qq.com']
	start_urls = ['http://v.qq.com/zt2012/2012yingchao/']
	# rules = (
	# 	#Rule(SgmlLinkExtractor(allow=(r'http://v.qq.com/zt2012/ligabbva/ligabbva\w+.htm>'))),
	# 	Rule(SgmlLinkExtractor(allow=(r'http://v.qq.com/zt2012/2012yingchao/(\w+)')), callback="parse"),
	# )
	s_round = 0;	# 赛事轮次
	is_over = False

	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		# 初始化最近赛事轮次
		if self.s_round == 0 and not self.is_over:	
			pre_last_url = "/html/body/div[@class='wrapper_zt']/div[@id='ztg_6']/div[@class='col_1']/div[@id='ztu_6']/div[@class='bd']/div[@class='inner']/div/table[@class='video_ct']/tbody/tr/td/div[@class='video_area']/table/tbody/tr[1]/td/div[@class='video_pic']/a/@href"
			pre_last = list_last_item(hxs.select(pre_last_url).extract())
			self.s_round = get_round('http://v.qq.com/zt2012/2012yingchao/2012yingchao(\w+).htm', pre_last)

		if self.s_round >= 0:
			if self.s_round > 0:
				next_link = 'http://v.qq.com/zt2012/2012yingchao/2012yingchao%02d.htm' % self.s_round
				if not RedisUtil.get(next_link):
					yield Request(url=next_link, callback=self.parse)
					# 使用redis保存已经爬取过的URL，避免重复爬行
					RedisUtil.set(next_link, next_link)

			sites = hxs.select("/html/body/div[@class='wrapper_zt']/div[@id='ztg_2']/div[@class='col_1']/div[@id='ztu_2']/div[@class='bd']/div[@class='inner']/div[@id='ztc_3']/div[@id='videoTV']/div[@class='right']/div[@id='videoListBox']/div[@id='videoList']/ul/li")
			items = []
			for site in sites:
				item = PremierleagueItem()
				item['sport_id'] = 3 # 英超
				item['s_round'] = self.s_round + 1
				item['title'] = list_first_item(site.select("h2/text()").extract())
				url = list_first_item(site.select("div/div[1]/dl/dd/span[@class='rightS']/a[@class='iconWb']/@onclick").extract())
				item['url'] = url.lstrip('postToWb(').rstrip(');').split(',')[2].strip("'")
				item['image'] = list_first_item(site.select("div/div[1]/dl/dt/img/@src").extract())
				item['time'] = list_first_item(site.select("div/div[1]/dl/dd/span[@class='time']/text()").extract()).rstrip('"')
				log.msg(item)
				yield item

			self.s_round -= 1
			if self.s_round == 0:
				self.is_over = True;