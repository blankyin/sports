#!/usr/bin/env python
# coding: utf-8

import web
import hashlib


def hash_password(password):
	return hashlib.sha1(password + 'a1').hexdigest()


def login_required(func):
	def function(*args):
		if not web.ctx.session.login:
			raise web.seeother('/')
		else:
			return func(*args)
	return function