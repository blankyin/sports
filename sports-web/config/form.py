#!/usr/bin/env python
# coding: utf-8

import web
from web import form

login_form = form.Form(
	form.Textbox("username", id="username", placeholder=u"用户名", description=u"用户名"),
	form.Password("password", id="password", placeholder=u"密码", description=u"密码"),
)