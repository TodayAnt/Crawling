# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 19:03:53 2020

@author: SeungHun Hyun
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#코드리스트 저장되있는 파일 불러와서 DF생성
os.chdir('C:\\Users\\SeungHun Hyun\\Anaconda3\\고웹\\Crawling')

import pymysql

db = pymysql.connect(
        user = 'root',
        passwd = '1234',
        host = '127.0.0.1',
        db = 'today_ant',
        charset= 'utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt, deletedAt)
    Values ('2', '엘앤에프','066970', {0}, {0}, {0});'''.format(now)



sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt, deletedAt)
        Values ('2', '엘앤에프','066970', 19981231235959,19981231235959,19981231235959);'''

cursor.execute(sql)
db.commit()



