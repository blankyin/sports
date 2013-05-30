#!/usr/bin/env python
# coding: utf-8
import web
import os
from config.jinja2_render import RenderJinja2

# 数据库连接
db = web.database(dbn='mysql', db='spider', host='127.0.0.1', user='root', pw='root')

# Jinja2模板加载
app_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 当前文件上级目录
templates_path = os.path.join(app_root, 'templates').replace('\\', '/')

render = RenderJinja2(
    templates_path,
    encoding='utf-8',
	registers=locals(),
	globals={'session': web.ctx.session}
)

web.config.debug = True


