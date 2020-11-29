# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 17:33:12 2020

@author: SeungHun Hyun
"""
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
os.chdir('C:\\Users\\SeungHun Hyun\\Anaconda3\\고웹\\Crawling')
chrome = webdriver.Chrome('chromedriver.exe')

chrome.get('https://finance.naver.com/item/main.nhn?code=005930')

#CSS셀렉터로 가져옴
#input_box = chrome.find_element_by_css_selector('#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input')
#print(input_box)
#input_box.send_keys('충북과학고등학교') #키를 보내는것
#input_box.send_keys(Keys.ENTER) #키가 가지고있는것중 엔터를 넣겟다.

price = chrome.find_element_by_css_selector('#content > ul > li:nth-child(2) > a > span')
print(price)
price.click()
                                            
                                            
                                            
                                            
                                            
                                            
link = chrome.find_element_by_css_selector('#rso > div:nth-child(1) > div > div.yuRUbf > a')
link.click()
#input_box.submit()
#time.sleep(3) # 3초간 정지

#chrome.quit() 
