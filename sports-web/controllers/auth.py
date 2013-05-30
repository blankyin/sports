#!/usr/bin/env python
# coding: utf-8


import web
from config import settings
from controllers.utils import hash_password

db = settings.db
table = 'auth_user'
render = settings.render

class Login:
	def GET(self):
		# 先检查是否有记住密码
		username = web.cookies().get('username')
		password = web.cookies().get('password')
		if username and password and self.checkUser(username, password):
			web.ctx.session.login = 1
			web.ctx.session.username = username
			return render.index()

		return render.render('auth/login')

	def POST(self):
		data = web.input()

		username = data.get('username','')
		password = data.get('password','')
		remember = data.get('remember', '')

		if not username or not password:
			data = {}
			data['username'] = username
			return render.render('auth/login')
		else:
			password = hash_password(password)

			if not self.checkUser(username, password):
				return render.render('auth/login')
			else:
				web.ctx.session.login = 1
				web.ctx.session.username = username

				# 记住密码一周
				if remember == 'on':
					expires = 7 * 24 * 60 * 60
					web.setcookie("username", username, expires)
					web.setcookie("password", password, expires)
				else:
					# 如果没有选择记住密码，清除cookie
					if web.cookies().get('username'):
						web.setcookie("username", username, -1)
					if web.cookies().get('password'):
						web.setcookie("password", password, -1)

				return web.seeother("/")

	def checkUser(self, username, password):
		""" 
		验证用户是否存在 
		"""
		user = db.query("select count(1) as count from auth_user where user_name=$username and password=$password and is_active=1", vars={'username':username, 'password':password})[0]
		if user.count < 1:
			return False
		else :
			return True


class Logout:
	"""
	注销登录，清除cookie
	"""
	def GET(self):
		web.ctx.session.kill()

		if web.cookies().get('username'):
			web.setcookie("username", '', -1)
		if web.cookies().get('password'):
			web.setcookie("password", '', -1)
		return web.seeother("/auth/login")