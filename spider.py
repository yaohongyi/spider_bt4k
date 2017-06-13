#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,re,pymysql

def get_film_url(num):
    '''
    :param num: num是24的倍数，起始值为24
    :return: 一个URL页面24部影片的访问地址
    '''
    url = 'http://www.bt4k.com/home-popular-list-version2017061212-offset0-count%d.js' % num
    bt_response = requests.get(url).content.decode('utf-8')
    pattern = re.compile(r'http:.*?(\d+).html?')
    page_num_list = re.findall(pattern, bt_response)
    film_url = []
    for i in page_num_list:
        film_url.append('http://www.bt4k.com/item/%s.html' % i)
    return film_url

def get_bt_url(url):
    '''
    :param url: 影片信息页面
    :return: 影片BT种子下载地址
    '''
    # 使用content.decode()替代text，避免了返回网页源码乱码问题
    bt_response = requests.get(url).content.decode('utf-8')
    # 获得影片名称
    film_name_pattern = re.compile('<div class="film_detail_name" itemprop="name">(.*)</div>')
    file_name = re.findall(film_name_pattern, bt_response)
    # 获得BT种子地址
    bt_pattern = re.compile('data-refb="(http:.*.torrent)"')
    bt_url = re.findall(bt_pattern, bt_response)

    film_info = {}
    film_info[file_name[0]] = str(bt_url[0])
    return film_info

def db_operate(data=None, operate_type='insert', **db_info):
    """
    :param data: 影片信息数据
    :param kwargs: 数据库连接信息
    :return:
    """
    conn = pymysql.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'],
                           passwd=db_info['passwd'], db=db_info['db'], charset=db_info['charset'])
    cur = conn.cursor()
    if operate_type == 'insert':
        sql = 'insert into film_info(name, bt_url) VALUES(%s, %s)'
        for i in data:
            cur.execute(sql, (i, data[i]))
        return
    if operate_type == 'select':
        sql = 'select * from film_info'
        # 执行查询语句，返回查询到多少条数据
        data_num = cur.execute(sql)
        if data_num:
            # 获取所有查询到的数据
            result = cur.fetchall()
            return result
        else:
            return None

    # 提交数据到数据库
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    # 获得24部影片的访问地址
    film_url = get_film_url(24)
    db_info = {'host':'127.0.0.1', 'port':3306, 'user':'root','passwd':'123456', 'db':'bt4k_film', 'charset':'utf8'}
    # 获得影片信息字典，包括影片名、bt种子地址
    # for i in film_url:
    #     single_film = get_bt_url(i)
    film_data = db_operate(operate_type='select' ,**db_info)
    for i in film_data:
        print(i)
