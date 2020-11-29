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
jongmokList = [] #선택된 종목 리스트

df_article = pd.DataFrame(columns=['headline'])#키워드를 포함한 기사 저장

df1 = pd.read_excel('관심종목.xlsx')
df1 = df1.fillna('0') # 결측치 0으로 처리
#관심종목을 딕셔너리 형태. 2차원 배열로
my_inter = {}
my_inter_list = []

for i in range(0, len(df1.columns)):
    my_inter_list.append(df1.columns[i])
    my_inter[df1.columns[i]] = list(df1.iloc[:,i])

#########################################1분 간격으로 반복#############################################
url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'

req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')#속보

subject = soup.findAll(class_='articleSubject')#헤드라인
summary = soup.findAll(class_='articleSummary')#기사요약, 시간


summary[0].text
title = [] #헤드라인 리스트
time = []
summary[0].find(class_='wdate').text

for i in range(0,20):
    title.append(subject[i].text.replace('\n','')) 
    time.append(summary[i].find(class_='wdate').text)
title
time


#DB에 저장된 관심종목, 키워드 포함하는 기사 데이터프레임에 저장.
for i in range(0,20): #키워드 포함시 저장, 한번 크롤링할때 기사 20개
    for jongmok in range(0,(len(my_inter_list))): #기사 하나당 관심종목 개수만큼 반복
        if(title[i].find(my_inter_list[jongmok])+1): #키워드 미포함시 -1을 반납하므로 +1해준다. 통과하면 관심종목명은 헤드라인에 포함된 것
            for keyword in range(0,len(my_inter.get(my_inter_list[jongmok]))): #해당 종목의 키워드 개수 만큼 반복
                if(title[i].find(my_inter.get(my_inter_list[jongmok])[keyword])+1):#종목명,키워드명 포함
                    df_article.loc[time[i]] = title[i] #중복된 기사는 더하지 않음.
                    jongmokList.append(my_inter_list[jongmok])
                    print('pass')














