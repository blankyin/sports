#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
    '/',						pre_fix + 'index.Index',
    '/video/(\w+)',				pre_fix + 'video.Video',
    '/auth/login',				pre_fix + 'auth.Login',
    '/auth/logout',				pre_fix + 'auth.Logout',
    '/article/article',			pre_fix + 'article.Article',
    '/article/article_detail',	pre_fix + 'article.ArticleDetail',
    '/article/add_article',		pre_fix + 'article.AddArticle',
    '/article/edit_article',    pre_fix + 'article.EditArticle',
    '/article/del_article',		pre_fix + 'article.DelArticle',
    '/article/category',		pre_fix + 'article.Category',
    '/article/del_category',	pre_fix + 'article.DelCategory',

)
