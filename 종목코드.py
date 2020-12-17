# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 17:00:10 2020

@author: SeungHun Hyun
"""
#DB itemCode 테이블에 종목과 코드 연동시켜 저장
import pandas as pd
import os
import pymysql
os.chdir('C:\\Users\\SeungHun Hyun\\Anaconda3\\고웹\\Crawling')

KS = pd.read_excel('코스피코드.xlsx')
KQ = pd.read_excel('코스닥코드.xlsx')
for i in range(0, len(KS)):#코드에 0붙여주기
    KS.iloc[i,0] = str(KS.iloc[i,0])
    while(len(KS.iloc[i,0])<6):
        KS.iloc[i,0] = '0' + KS.iloc[i,0]    
for i in range(0, len(KQ)):#코드에 0붙여주기
    KQ.iloc[i,0] = str(KQ.iloc[i,0])
    while(len(KQ.iloc[i,0])<6):
        KQ.iloc[i,0] = '0' + KQ.iloc[i,0]    
db = pymysql.connect(
        user = 'root',
        passwd = '1234',
        host = '127.0.0.1',
        db = 'today_ant',
        charset= 'utf8'
)
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = '''CREATE TABLE `itemCode` (
`id` int(10) NOT NULL AUTO_INCREMENT,
`item` varchar(30) NOT NULL,
`code` varchar(15) NOT NULL,
PRIMARY KEY(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
cursor.execute(sql) 

for i in range(0, len(KS)):
    sql = '''INSERT INTO `itemCode` (item, code) Values ('{0}', '{1}');'''.format(KS.loc[i,'기업명'],KS.loc[i,'종목코드'])
    cursor.execute(sql)
for i in range(0, len(KQ)):
    sql = '''INSERT INTO `itemCode` (item, code) Values ('{0}', '{1}');'''.format(KQ.loc[i,'기업명'],KQ.loc[i,'종목코드'])
    cursor.execute(sql)

db.commit()




