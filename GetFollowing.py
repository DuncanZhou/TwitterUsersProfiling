#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import requests
import json
import time
import random
import urllib2
import re
from BeautifulSoup import BeautifulSoup
import MySQLdb as mysql
import cookielib
import urllib
import threading

def crawlDetailPage(url):
    # 使用代理ip
    proxy ={'http':"http://183.159.91.135:18118",
            'http':'http://183.128.32.204:18118',
            'http':'http://125.127.158.162:61234',
            'https':'https://60.177.226.43:18118',
            'http':'http://111.183.231.253:61234'}
    ids = set()
    req = requests.get(url,proxies=proxy)
    jsondata = req.text
    data = json.loads(jsondata)

    content = data['data']['cards']

    for i in content:
        followingId = i['user']['id']
        ids.add(str(followingId))
    return ids

# 解析cookie
def ParseCookie(cookie):
    res = {}
    cookies = cookie.split(";")
    for cook in cookies:
        key,value = cook.split("=")
        res[key.lstrip().rstrip()] = value.lstrip().rstrip()
    return res

def GetContainerId(id):
    url = "https://weibo.com/" + id
    cookies = "SINAGLOBAL=4043605503975.1895.1479819188716; UM_distinctid=1621ef12ef35c9-010737f44f7c2d-3a75045d-1fa400-1621ef12ef45eb; _s_tentry=ent.ifeng.com; YF-V5-G0=b1e3c8e8ad37eca95b65a6759b3fc219; Apache=1879352856775.3337.1523458056359; ULV=1523458056368:63:1:1:1879352856775.3337.1523458056359:1522138879467; YF-Page-G0=ee5462a7ca7a278058fd1807a910bc74; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; login_sid_t=bbb9fec459ca99f483b3f769202275a0; cross_origin_proto=SSL; wb_cmtLike_6050650176=1; appkey=; WBtopGlobal_register_version=25c556e6eb9b606e; un=13776120509; WBStorage=96e2695964e412de|undefined; UOR=baike.baidu.com,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWjTyGjFD-0cyZI7kC7IYg5JpX5K2hUgL.Foe4S0eEShM0Sh22dJLoI0YLxKBLBonL1h5LxK-L1hnL1hMLxK.L1heLB.x4ICH8Sb-4SEHWeFH8Sb-R1C-ReFH81FHFeF-4e05pe8Yf1K-t; ALF=1556764397; SSOLoginState=1525228398; SCF=An2pxqirryGJ7asCvq8npDbZpxwysghsp8yKuZvilRtrh0zFAoo3eBbnLn1KC2mL_lo4_H_nCbctjb0sJ3ONd8k.; SUB=_2A2537VM-DeRhGeVH7FET9CnPzz2IHXVUm8P2rDV8PUNbmtBeLW7hkW9NTv9QmISskVXtb_jtCvl7DXUn8lSW3Exb; SUHB=0RyaX0Q7gYyzxE; wvr=6"
    cookies = ParseCookie(cookies)
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive',
               # 'Host': 'weibo.com',
               'Upgrade-Insecure-Requests': '1',
               'Refer': "https://weibo.com/"
               }
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # 先获取cookie
    login = {"username":"13776120509","password":"aaasssddd"}
    # res = opener.open("https://weibo.com")
    # for item in cj:
    #     print item.name + " " + item.value

    # cj.set_cookie(cookies)
    post_data = urllib.urlencode(login)
    # print headers
    req = urllib2.Request(url,post_data,headers)
    # response = urllib2.urlopen(req)
    response = urllib2.urlopen(req)
    data = response.read()
    # print data
    soup = BeautifulSoup(data)
    results = soup.findAll("script",attrs={'type':'text/javascript'})
    string = str(results)
    r = re.findall(r"\[\'page_id\'\]=\'(\d+)\'",string)
    return r[0]

def GetFollowing(pid):
    db = mysql.connect(host="192.168.131.191",port=3306,db="weibo", user="root",passwd="", charset='utf8' )
    cursor = db.cursor()

    cursor.execute("select id from users")
    total_ids = set()
    results = list(cursor.fetchall())
    for res in results:
        total_ids.add(res[0])
    famous_ids = set()
    cursor.execute("select id from users where category != 'Common'")
    results = list(cursor.fetchall())
    for res in results:
        famous_ids.add(res[0])
    count = 0
    period = len(famous_ids) / 10
    start = (pid - 1) * period
    end = pid * period
    # 对famous抓取关注的用户列表
    for id in famous_ids:
        # 先获取container_id
        count += 1
        if count <= 65 or count < start:
            continue
        if count > end:
            break
        # 如果数据库中有了则跳过
        cursor.execute("select count(*) from relationships where suid = '%s'" % id)
        results = cursor.fetchone()
        if results[0] >= 1:
            continue
        following = Following(str("100505" + id))
        # 在数据库中的,插入到target_db中
        following &= total_ids
        print len(following)
        for tuid in following:
            cursor.execute("insert into relationships(suid,tuid) values('%s','%s')" % (id,tuid))
        db.commit()

        print "已完成%d个用户" % count
        # time.sleep(random.choice([0,1,2,3,4,5]))

    cursor.close()
    db.close()

# 得到关注列表
def Following(uid):

    print "正在获取%s用户的关注列表" % uid
    following = set()
    url = "https://m.weibo.cn/api/container/getSecond?containerid=%s_-_FOLLOWERS&page=" % uid
    pageid = 1
    flag = True
    while flag:
        try:
            following |= crawlDetailPage(url+str(pageid))
            time.sleep(random.choice([1,2,3,4]))
            pageid += 1
            print "第%d页" % pageid
            if pageid > 100:
                break
        except Exception as e:
            flag = False
    return following

# i/o密集型应该使用多线程
def run():
    pid = 1
    while pid <= 10:
        t = threading.Thread(target=GetFollowing,args=(pid,))
        t.start()
        pid += 1
run()

# GetFollowing(1)
# Following("1005053973247341")