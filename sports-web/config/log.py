#!/usr/bin/env python
# coding: utf-8

from wsgilog import WsgiLog

class Log(WsgiLog):
	def __init__(self, application):
		WsgiLog.__init__(
			self, 
			application, 
			# logformat = '%(message)s',
			tofile = True,
			toprint = True,
			tostream = True,
			file = 'logs/wsgilog.log',
			interval = 'h',	# 日志文件备份间隔时间单位
			backups = 24		# 日志文件备份间隔时间
			)