# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import datetime # 引入日期时间模块

def getPage(url):#获取链接中的网页内容
    headers = {
        "X-Infinitescroll": "true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    return requests.get(url=url, headers=headers).content
soup = BeautifulSoup(getPage('https://www.jianshu.com/p/097e72fac81e'),"lxml")
user_list={}
article={}
for i in soup.select("td a"):
    user_list[i.get_text()]=i.get('href')
print(user_list)
# 控制爬取用户数
n=0
for key,value in user_list.items():
    tempsoup1=BeautifulSoup(getPage(value), "lxml")
    for i in tempsoup1.select('.title'):
        tempsoup2=BeautifulSoup(getPage('https://www.jianshu.com'+i.get('href')),"lxml")
        temp1=""
        for i in tempsoup2.select('.show-content-free p'):
            temp1=temp1+i.get_text()
        article[tempsoup2.select('.title')[0].get_text()]=temp1
    n+=1
    if(n==10):
        break
for key,value in article.items():
    try:
        f = open(key+'.txt','w', encoding='utf-8')
        f.write(key + '\n' + value)
    finally:
        if f:
            f.close()