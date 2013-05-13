项目名称：
============================
sports


项目目的：
============================
1. 爬取欧洲足球几大联赛（西甲、英超、意甲）每轮比赛精彩集锦，视频源：http://v.qq.com/sports/
2. 爬取中超每轮比赛精彩集锦，视频源：http://sports.sina.com.cn/video/c/j/csl/


项目背景：
============================
1. scrapy + mysql + redis
2. 第一个scrapy项目
3. 开发中使用了chrome插件XPath Helper，方便XPath解析
4. 使用redis保存已经爬取过的URL，避免重复爬取
5. 数据保存在mysql数据库，插入时判断数据是否重复


避免爬虫被禁的策略：
============================
1. 禁用cookie（COOKIES_ENABLED）
2. 下载延迟（DOWNLOAD_DELAY）
3. 实现一个download middleware，不停的变user-aget（ChangeUserAgentMiddleware）
4. 使用Google搜索引擎的延迟，而不是直接访问站点（默认关闭 GoogleCacheMiddleware）
5. 使用一个可以循环利用的IP池 （默认关闭，还需完善	ProxyMiddleware）


通过使用scrapyd同时运行多个爬虫：
============================
1. 定制命令（sports.commands.allcrawl）
2. settings.py中配置 COMMANDS_MODULE = 'sports.commands'
3. 运行scrapyd: scrapy server 
	参考：	http://plotcup.com/a/108 和 http://scrapyd.readthedocs.org/en/latest
4. 运行 scrapy allcrawl 