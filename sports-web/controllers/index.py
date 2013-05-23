#!/usr/bin/env python
# coding: utf-8

import web
from config import settings

render = settings.render

class Index:
	def GET(self):
		data = {}
		print web.ctx.session.login
		print web.ctx.session.username
		return render.index(data)
