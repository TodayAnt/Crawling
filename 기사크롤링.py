# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:02:07 2020

@author: SeungHun Hyun
"""
#기사가 나온 시간 시세 크롤링 셀레니움
#DB연동

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pymysql
jongmokList = [] #선택된 종목 리스트

#df_article = pd.DataFrame(columns=['headline', 'summary', 'interest_id', 'upload_time', 'createdAt'])#키워드를 포함한 기사 저장
#df1 = pd.read_excel('관심종목.xlsx')
#df1 = df1.fillna('0') # 결측치 0으로 처리

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
#sql = '''SELECT * FROM itemcode WHERE item='엘앤에프';'''
cursor.execute(sql) 
result = cursor.fetchall()
#code = result[0]['code']
df = pd.DataFrame(result)
df = df.set_index('item')
del df['id']


#관심종목 테이블 접근
sql = "SELECT * FROM `interests`;"
cursor.execute(sql)
result = cursor.fetchall()
interests = pd.DataFrame(result)
interests = interests.set_index('item')
len(interests)

#키워드 테이블 접근
sql = "SELECT * FROM `keywords`;"
cursor.execute(sql)
result = cursor.fetchall()
keywords = pd.DataFrame(result)
len(keywords)

interests.loc[3,'item'] # 기업명
interests.loc[3,'id'] #id
keywords.loc[0,'interest_id']
keywords.loc[0,'name']


#########################################1분 간격으로 반복#############################################
url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'

req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')#속보

subject = soup.findAll(class_='articleSubject')#헤드라인
article = soup.findAll(class_='articleSummary')#기사요약, 시간

sliceSum = article[0].text.find('...\n\t')
article[0].text[:sliceSum].replace('\n', '').replace('\t', '')
title = [] #헤드라인 리스트
time = []#시간
summary = []#기사요약

for i in range(0,20):
    title.append(subject[i].text.replace('\n','')) 
    time.append(article[i].find(class_='wdate').text)
    sliceSum = article[i].text.find('...\n\t')
    summary.append(article[i].text[:sliceSum].replace('\n', '').replace('\t', ''))
title
time
summary


columns=['headline', 'summary', 'interest_id', 'upload_time', 'createdAt']

for i in range(0,20):#한번 크롤링할때 기사 20개
    for key in range(0,  len(keywords)):#키워드길이만큼 반복
        if(title[i].find(keywords.loc[key,'name'])+1): #타이틀에 키워드 미포함시 -1리턴하므로 +1해줌
            interest_id = keywords.loc[key,'interest_id']
            sql = 'select * from interests where id=%d'%(interest_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            if(result):#종목명, 키워드 모두 포함했을때 posts에 추가
#                df_article.loc[time[i]] = [title[i], summary[i], interest_id, time[i], ''] #중복된 기사는 더하지 않음.
                print('있다')
                now = str(datetime.datetime.now())
                now = now[:19]
                createdAt = now.replace('-', '').replace(':','').replace(' ', '')
                time[i] = time[i]+'00'
                time[i] = time[i].replace('-', '').replace(':','').replace(' ', '')
                len(createdAt)
                time[i]
                createdAt
                print(title[i])
                print(summary[i])
                time[i]
                user_id = 2
                sql = '''INSERT INTO `posts` (user_id, interest_id, headline, summary, upload_time, createdAt, updatedAt)
                Values ({5}, '{0}', '{1}', '{2}', {3}, {4}, {4});'''.format(interest_id, title[i], summary[i],time[i], createdAt, user_id)
                cursor.execute(sql)
db.commit()



result[0]['interest_id']
result[0]['id']
result[0]
for i in range(0, len(result)):#포스트에 있는 interest_id로 종목코드 추출->현재가 크롤링후 업뎃
    interest_id = result[i]['interest_id']
    sql = 'select * from interests where id = %d;'%(interest_id)
    cursor.execute(sql)
    codeInfo = cursor.fetchall()
    code = codeInfo[0]['code']    
    
    url = 'https://finance.naver.com/item/main.nhn?code='+ code
    req = requests.get(url)
    html = req.text
    
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find(class_ = 'no_today')#현재가
    price = price.find(class_='blind')
    price = price.text.replace(',', '')
    
    sql = 'UPDATE `posts` SET cur_price = {0} WHERE interest_id = {1};'.format(price, interest_id)
    cursor.execute(sql)
    db.commit()
#    fluct = soup.find(class_ = 'no_exday')#등락률
#    fluct = fluct.findAll(class_='blind')[1]
#    fluct = fluct.text
#    

sql = 'select * from posts;'
cursor.execute(sql)
result = cursor.fetchall()
result

            
#
##현재시간
#now = str(datetime.datetime.now())
#now = now[:19]
#createdAt = now.replace('-', '').replace(':','').replace(' ', '')
#createdAt
##기업명과 코드 연결
#name = '예선테크'
#code = df.loc[name,'code']
##포스트추가
#sql = '''INSERT INTO `posts` (user_id, interest_id, headline, upload_time, createdAt, updatedAt)
#    Values ('2', '{0}', {1}, {2}, {2});'''.format(interest_id, headline, upload_time, createdAt)
#
##관심종목추가
#
#sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt)
#    Values ('2', '{0}', {1}, {2}, {2});'''.format(name, code, createdAt)
##sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt)
##    Values ('2', '예선테크', {1}, {0}, {0});'''.format(createdAt, code)
#
#interest_id = interests.loc[name].id
#keyword = 'OLED'
##키워드추가
#    
#sql ='''INSERT INTO `keywords` (interest_id, name, createdAt, updatedAt)
#        Values({0}, '{1}', {2}, {2});'''.format(interest_id, keyword,createdAt)
##
#cursor.execute(sql)
#db.commit()
















