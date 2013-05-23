#!/usr/bin/env python
# coding: utf-8

from config.url import urls
import web

app = web.application(urls, globals())

if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store, initializer={'login':False, 'username':''})
	web.config._session = session
else:
	session = web.config._session

def session_hook():
	web.ctx.session = session

def request_hook():
	request = {}
	request['username'] = web.ctx.session.username
	web.ctx.request = request

app.add_processor(web.loadhook(session_hook))
app.add_processor(web.loadhook(request_hook))


if __name__ == "__main__":
    app.run()
