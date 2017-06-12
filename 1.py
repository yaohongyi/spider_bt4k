#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,re

num = 24
plus_num = 24
url = 'http://www.bt4k.com/home-popular-list-version2017061212-offset0-count%d.js' % num
bt_response = requests.get(url).text
pattern = re.compile(r'http:.*?(\d+).html?')
# 提取出电影访问页面的编号
result = re.findall(pattern, bt_response)
# http://www.bt4k.com/item/887.html
for i in result:
    print('http://www.bt4k.com/item/%s.html' % i)
