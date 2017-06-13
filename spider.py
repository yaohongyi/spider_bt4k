#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests,re,pymysql,time
import threading

def get_film_url(num):
    '''
    :param num: num是24的倍数，起始值为24
    :return: 一个URL页面24部影片的访问地址
    '''
    # 获取当前年月日时，格式例如：2017061310
    now = time.strftime("%Y%m%d%H", time.localtime())
    url = 'http://www.bt4k.com/home-popular-list-version%s-offset%d-count24.js' % (now, num)
    # bt_response = requests.get(url).content.decode('utf-8')
    bt_response = requests.get(url).text
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

def db_insert(data, **db_info):
    """
    :param data: 影片信息数据
    :param kwargs: 数据库连接信息
    :return:
    """
    conn = pymysql.connect(host=db_info['host'], port=db_info['port'], user=db_info['user'],
                           passwd=db_info['passwd'], db=db_info['db'], charset=db_info['charset'])
    cur = conn.cursor()
    sql = 'insert into film_info(name, bt_url) VALUES(%s, %s)'
    try:
        for i in data:
            cur.execute(sql, (i, data[i]))
        # 提交数据到数据库
        conn.commit()
        print('.')
    except:
        pass
    # 关闭游标
    cur.close()
    # 关闭数据库连接
    conn.close()

def db_select(**db_info):
    conn = pymysql.connect(db_info['host'], db_info['port'], db_info['user'],
                           db_info['passwd'], db_info['db'], db_info['chrset'])
    cur = conn.cursor()
    cur.execute('select * from film_info')
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

def main():
    # 数据库连接信息
    db_info = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': '123456', 'db': 'bt4k_film',
               'charset': 'utf8'}
    start_num = 24
    end_num = 24
    while start_num <= end_num:
        film_url = get_film_url(start_num)
        for i in film_url:
            print('.',)
            single_film = get_bt_url(i)
            db_insert(data=single_film, **db_info)
        start_num += 24

if __name__ == '__main__':
    main()
