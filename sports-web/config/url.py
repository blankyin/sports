#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',					pre_fix + 'index.Index',
    '/video/(\w+)',			pre_fix + 'video.Video',

)
