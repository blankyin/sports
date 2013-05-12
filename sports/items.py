#-*-coding:utf-8-*-

from scrapy.item import Item, Field

class VideoItem(Item):
	sport_id = Field()
	s_round = Field()
	title = Field()
	url = Field()
	image = Field()
	time = Field()


class LaligaItem(VideoItem):
    """ 西甲 """
    pass


class PremierleagueItem(VideoItem):
	""" 英超 """
	pass

class SerieaItem(VideoItem):
	""" 意甲 """
	pass
