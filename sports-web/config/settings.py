#!/usr/bin/env python
# coding: utf-8
import web
import os
from web.contrib.template import render_jinja

db = web.database(dbn='mysql', db='spider', host='127.0.0.1', user='root', pw='root')

#render = web.template.render('templates/', cache=False)
#render_layout = web.template.render('templates/', base='layout', cache=False)

# Jinja2模板加载
app_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 当前文件上级目录
templates_path = os.path.join(app_root, 'templates').replace('\\', '/')
render = render_jinja(
    templates_path,
    encoding='utf-8'
)

config = web.storage(
    email='blankyin@gmail.com',
    site_name = '体育视频',
    site_desc = '',
    static = '/static',
)


web.config.debug = True

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render

