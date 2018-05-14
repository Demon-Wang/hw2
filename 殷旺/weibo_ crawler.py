import requests
from bs4 import BeautifulSoup

# 引入库
def getPage(url):#获取链接中的网页内容
    headers = {
        "X-Infinitescroll": "true",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    return requests.get(url=url, headers=headers).content
# 每页用户数为10 num为爬取开始页面
num=1
user = {}
while(True):
    page = getPage('https://weibo.cn/pub/top?cat=star&page=%d'%num)
        # 将基础网址和页数拼接得到实际网址，使用request的get方法获取响应，再用content方法得到内容
    soup = BeautifulSoup(page,'lxml')
        # 使用BeautifulSoup分析页面，这里并没有指定解析器，会自动选取可获得的最优解析器
        # BeautifulSoup会报一个warning要你选择解析器，可以忽略
    for i in soup.select(".nk"):
        user[i.get_text()] = i.get('href')
    num+=1
    if(num==11):
        break

view={}
for key,value in user.items():
    tempsoup=BeautifulSoup(getPage(value),"lxml")
    temstr=""
    for i in tempsoup.select('.c .ctt'):
        temstr+=i.get_text()+'\n'
    view[key]=temstr
for key,value in view.items():
    try:
        f = open(key+'.txt','w', encoding='utf-8')
        f.write(key + '\n' + value)
    finally:
        if f:
            f.close()
