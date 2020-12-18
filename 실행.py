# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 13:41:20 2020

@author: SeungHun Hyun
"""

import requests, json
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pymysql
import schedule
import time

#DB 테이블 접근
db = pymysql.connect(
        user = 'root',
        passwd = '1234',
        host = '127.0.0.1',
        db = 'today_ant',
        charset= 'utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)
#종목명-코드 연동 데이터 불러오기
sql = 'SELECT * FROM itemcode;'
cursor.execute(sql) 
result = cursor.fetchall()
df = pd.DataFrame(result)
df = df.set_index('item')
del df['id']
#관심종목 테이블 접근
sql = "SELECT * FROM `interests`;"
cursor.execute(sql)
result = cursor.fetchall()
interests = pd.DataFrame(result)
interests = interests.set_index('item')

#schedule.every(3000).seconds.do(checker = [])
#checker = []#title확인용. 한번크롤링할때마다 리스트에 타이틀append
#crawlArticle()
#crawlPrice()
#30초에 한번씩 실행
schedule.every(30).seconds.do(crawlArticle)
schedule.every(30).seconds.do(crawlPrice)
while True: 
    schedule.run_pending() 
    time.sleep(1)


#관심종목수동추가
#now = str(datetime.datetime.now())
#now = now[:19]
#createdAt = now.replace('-', '').replace(':','').replace(' ', '')#추가시각
#createdAt
#name = '파미셀'
#code = str(df.loc[name,'code'])
#keyword1 = '공급계약'
##keyword2 = ''
#sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt, keyword1)
#    Values ('2', '{0}', '{1}', {2}, {2}, '{3}');'''.format(name, code, createdAt, keyword1)
#cursor.execute(sql)
#db.commit()
