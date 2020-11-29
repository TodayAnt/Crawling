# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 16:00:27 2020

@author: SeungHun Hyun
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#코드리스트 저장되있는 파일 불러와서 DF생성
os.chdir('C:\\Users\\SeungHun Hyun\\Anaconda3\\고웹\\Crawling')
df = pd.read_excel('종목코드.xlsx')
df.columns = ['name', 'number']
df = df.set_index('name')


############################################1분간격 반복#############################
jongmokList1 = set(jongmokList)
jongmokList = list(jongmokList1)
codeList = []


for i in range(0, len(jongmokList)):
    codeList.append(df.loc[jongmokList[i],:].number[1:])#'뺌



for i in range(0, len(codeList)):
    url = 'https://finance.naver.com/item/main.nhn?code='+ codeList[i]
    req = requests.get(url)
    html = req.text
    
    soup = BeautifulSoup(html, 'html.parser')
    price = soup.find(class_ = 'no_today')#현재가
    price = price.find(class_='blind')
    price = price.text.replace(',', '')
    
    fluct = soup.find(class_ = 'no_exday')#등락률
    fluct = fluct.findAll(class_='blind')[1]
    fluct = fluct.text
    
    print('종목 : '+jongmokList[i]+' 현재가 : '+price+' 등락률 : '+fluct+'%\n헤드라인 : '
          +df_article.iloc[i,0]+ ' 시간 : '+df_article.index[i])







