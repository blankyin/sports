#!/usr/bin/env python
# coding: utf-8

from config import settings

render = settings.render

class Index:
	def GET(self):
		data = {}
		return render.index(data)
