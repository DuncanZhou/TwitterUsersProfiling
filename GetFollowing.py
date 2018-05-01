import requests
import json
import time
import random
import urllib2
import re
from BeautifulSoup import BeautifulSoup

def crawlDetailPage(url,page):
    ids = set()
    #读取微博网页的JSON信息
    req = requests.get(url)
    jsondata = req.text
    data = json.loads(jsondata)

    #获取每一条页的数据
    content = data['cards']
    #print(content)

    #循环输出每一页的关注者各项信息
    for i in content:
        followingId = i['user']['id']
        ids.add(followingId)

def GetContainerId(id):
    url = "https://weibo.com/" + id
    headers = {'Accept': '*/*',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               'Referer': 'http://www.baidu.com/'
               }
    req = urllib2.Request(url,None,headers)
    response = urllib2.urlopen(req)
    data = response.read()
    soup =
    soup.findAll("script",attrs={'type':'text/javascript'})
    r = re.findall(r"\[\'page_id\'\]=\'(\d+)\'",string)



for i in range(1,11):
    print("正在获取第{}页的关注列表:".format(i))
    #微博用户关注列表JSON链接
    url = "https://m.weibo.cn/api/container/getSecond?containerid=1005052164843961_-_FOLLOWERS&page=" + str(i)
    crawlDetailPage(url,i)
    #设置休眠时间
    t = random.randint(31,33)
    print("休眠时间为:{}s".format(t))
    time.sleep(t)