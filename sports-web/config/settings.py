#!/usr/bin/env python
# coding: utf-8
import web

db = web.database(dbn='mysql', db='spider', host='127.0.0.1', user='root', pw='root')

render = web.template.render('templates/', base='layout', cache=False)

web.config.debug = True

config = web.storage(
    email='blankyin@gmail.com',
    site_name = '体育视频',
    site_desc = '',
    static = '/static',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
