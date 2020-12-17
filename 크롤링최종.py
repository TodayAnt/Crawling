# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:02:07 2020

@author: SeungHun Hyun
"""
#기사가 나온 시간 시세 크롤링 셀레니움
#DB연동

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


#checker = []#title 확인용
#########################################1분 간격으로 반복#############################################
def crawlArticle():
    url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')#속보
    subject = soup.findAll(class_='articleSubject')#헤드라인
    article = soup.findAll(class_='articleSummary')#기사요약, 시간
    sliceSum = article[0].text.find('...\n\t')
    article[0].text[:sliceSum].replace('\n', '').replace('\t', '')
    title = [] #헤드라인 리스트
    timeArticle = []#시간
    summary = []#기사요약
    
    for i in range(0,20):
        title.append(subject[i].text.replace('\n','').replace('\'', ''))
        timeArticle.append(article[i].find(class_='wdate').text)
        sliceSum = article[i].text.find('...\n\t')
        summary.append(article[i].text[:sliceSum].replace('\n', '').replace('\t', '').replace('\'', ''))
#    title[19] = '상폐, 코오롱티슈진'
#    checker.append(title)
    sql = 'select * from interests'#관심종목 DB로
    cursor.execute(sql)
    result = cursor.fetchall()
    now = str(datetime.datetime.now()) 
    now = now[:19]
    createdAt = now.replace('-', '').replace(':','').replace(' ', '')#생성된시간
    
    for i in range(0,20):#한번 크롤링할때 기사 20개
        for inter in range(0,  len(result)):#관심종목길이만큼 반복
            if(title[i].find(result[inter]['item'])+1): #타이틀에 관심종목명 미포함시 -1리턴하므로 +1해줌        
                timeArticle[i] = timeArticle[i]+'00'#date 형식 맞추기위해서
                timeArticle[i] = timeArticle[i].replace('-', '').replace(':','').replace(' ', '')
                for j in range(0,10):#키워드는 최대10개이므로 반복
                    if(result[inter]['keyword%d'%(j+1)]):#키워드가 존재하면.
                        sql = 'SELECT * FROM posts;' #포스트에 중복된게 있는지 확인해야함.
                        cursor.execute(sql) 
                        resultPost = cursor.fetchall()
                        num = -1
                        num = title[i].find(result[inter]['keyword%d'%(j+1)])#타이틀안에 키워드가 존재.
#                        print(result[inter]['keyword%d'%(j+1)])
#                        print(num)
                        if(num>-1):
                            interest_id = result[inter]['id']
                            keyword_num = j+1
                            user_id = result[inter]['user_id']
                            if (len(resultPost)==0):#포스트에 아무것도없으면 중복체크 안해도 됌
                                print('pass1')                        
                                sql = '''INSERT INTO `posts` (user_id, interest_id, keyword_num,headline, summary, upload_time, createdAt, updatedAt)
                                Values ({0}, {1},{2}, '{3}', '{4}', {5}, {6}, {6});'''.format(user_id, interest_id, keyword_num, title[i], summary[i],timeArticle[i], createdAt)
                                cursor.execute(sql)
                                db.commit()
                                continue
                            count = 0
                            for post in range(0, len(resultPost)):#포스트리스트에서 겹치는거 있으면 인서트안함.                                
                                if(resultPost[post]['keyword_num'] == keyword_num and resultPost[post]['interest_id']== interest_id) :
                                    count+=1
                            if(count==0):#모든 포스트리스트에서 겹치는게 없다면 추가
                                print('pass2')                 
                                sql = '''INSERT INTO `posts` (user_id, interest_id, keyword_num,headline, summary, upload_time, createdAt, updatedAt)
                                Values ({0}, {1},{2}, '{3}', '{4}', {5}, {6}, {6});'''.format(user_id, interest_id, keyword_num, title[i], summary[i],timeArticle[i], createdAt)
                                cursor.execute(sql)
                                db.commit()    

def crawlPrice():                                   
    sql = 'SELECT * FROM posts;'
    cursor.execute(sql) 
    resultPost = cursor.fetchall()
    for i in range(0, len(resultPost)):#포스트에 있는 interest_id로 종목코드 추출->현재가 크롤링후 업뎃
        interest_id = resultPost[i]['interest_id']
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
        fluct = soup.find(class_ = 'no_exday')#등락률
        fluct = fluct.findAll(class_='blind')[1]
        fluct = fluct.text
        sql = 'UPDATE `posts` SET cur_price = {0} WHERE interest_id = {1};'.format(fluct, interest_id)
        cursor.execute(sql)
    db.commit()

#crawlArticle()
#crawlPrice()
schedule.every(30).seconds.do(crawlArticle)
schedule.every(30).seconds.do(crawlPrice)
while True: 
    schedule.run_pending() 
    time.sleep(1)


##현재시간
#now = str(datetime.datetime.now())
#now = now[:19]
#createdAt = now.replace('-', '').replace(':','').replace(' ', '')
#createdAt
#
#
##기업명과 코드 연결
#name = '한진중공업'
#code = df.loc[name,'code']
##포스트추가
#sql = '''INSERT INTO `posts` (user_id, interest_id, headline, upload_time, createdAt, updatedAt)
#    Values ('2', '{0}', {1}, {2}, {2});'''.format(interest_id, headline, upload_time, createdAt)
#
##관심종목추가
#keyword = '컨소시엄'
#sql = '''INSERT INTO `interests` (user_id, item, code, createdAt, updatedAt, keyword1)
#    Values ('2', '{0}', {1}, {2}, {2}, '{3}');'''.format(name, code, createdAt, keyword)
##키워드추가
#keyword2 = '인보사'
#interest_id = 4
#sql = '''UPDATE `interests` SET keyword2 = '{0}' WHERE id = {1};'.format(keyword2, interest_id)'''
#cursor.execute(sql)
#
#cursor.execute(sql)
#db.commit()
#
#
#
#
#
#
#
#
#
