#-*-coding:utf-8-*-

import re

def get_round(match_rule, match_url):
	""" 根据URL获取赛事赛程 """
	if match_rule and match_url:
		m = re.match(match_rule, match_url)
		if m and m.groups():
			return int(m.groups()[0])
	
	return -1