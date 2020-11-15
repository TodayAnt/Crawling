# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 19:02:07 2020

@author: SeungHun Hyun
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://finance.naver.com/news/news_list.nhn?mode=LSS2D&section_id=101&section_id2=258'

url1 = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1=001'
req = requests.get(url)
html = req.text
soup = BeautifulSoup(html, 'html.parser')
subject = soup.findAll(class_='articleSubject')
summary = soup.findAll(class_='articleSummary')
print(summary)
print(summary[0])
summary[0]
title=[] #헤드라인 리스트
time = []
article_summary = []
type(summary[0])
summary[0].find(class_='wdate').text
for i in range(0,20):
    title.append(subject[i].text) 
    time.append(summary[i].find(class_='wdate').text)
title
time
print(subject[0].a)
href = str(subject[0].a)
print(href)
slice_at = href.find('title')
href = href[9:slice_at-2]
href = 'https://finance.naver.com'+href
print(href)
#inm src 같은걸 어트리뷰트라 한다.
