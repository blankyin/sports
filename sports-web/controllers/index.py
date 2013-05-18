#!/usr/bin/env python
# coding: utf-8

from config import settings

render_layout = settings.render_layout

class Index:
	def GET(self):
		
		return render_layout.index()
