#-*-coding:utf-8-*-

import base64
import random

class ProxyMiddleware(object):

	PROXIES = [ 
				{'ip_port': '127.0.0.1:3333', 'user_pass': 'foo:bar'},
			   	{'ip_port': '127.0.0.2:4444', 'user_pass': 'username:password'},
			   	{'ip_port': '127.0.0.3:5555', 'user_pass': ''},
			  ]

	def process_request(self, request, spider):
		proxy = random.choice(self.PROXIES)
		if proxy['user_pass'] is not None:
			request.meta['proxy'] = "http://%s" % proxy['ip_port']
			encoded_user_pass = base64.encodestring(proxy['user_pass'])
			request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
		else:
			request.meta['proxy'] = "http://%s" % proxy['ip_port']