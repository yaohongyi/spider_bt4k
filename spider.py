#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,re

def get_film_url(num):
    '''
    :param num: num是24的倍数，起始值为24
    :return: 一个URL页面24部影片的访问地址
    '''
    url = 'http://www.bt4k.com/home-popular-list-version2017061212-offset0-count%d.js' % num
    bt_response = requests.get(url).text
    pattern = re.compile(r'http:.*?(\d+).html?')
    page_num_list = re.findall(pattern, bt_response)
    film_url = []
    for i in page_num_list:
        film_url.append('http://www.bt4k.com/item/%s.html' % i)
    return film_url

def get_film_info(url):
    bt_response = requests.get(url).content.decode('utf-8')
    # print(bt_response)
    # 获得影片名称
    film_name_pattern = re.compile('<meta property="og:video:alias" content="(.*)"/>')
    file_name = re.findall(film_name_pattern, bt_response)
    # 获得BT种子地址
    bt_pattern = re.compile('data-refb="(http:.*.torrent)"')
    bt_url = re.findall(bt_pattern, bt_response)
    print(bt_url[0])

    film_info = []
    film_info[file_name] = bt_url[0]
    return film_info

if __name__ == '__main__':
    # film_url = get_film_url(24)
    url = 'http://www.bt4k.com/item/902.html'
    print(get_film_info(url))
