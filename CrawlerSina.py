#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import requests
from selenium import webdriver
from BeautifulSoup import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pickle
import time
import re

_APP_KKEY = '4195913424'
_APP_SECRET = 'bfd3599417dd9edea9441b1e30ede136'
_ACCESS_TOKEN = '2.00sVuTbGykcxZEf71138a198VHry5E'
_REDIRECT_URL = 'http://api.weibo.com/oauth2/default.html'

class Crawler:
    def __init__(self):
        pass

    # 登录
    def login(self):
        login_url = "http://weibo.com/login.php"
        # login_url = "https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F"
        account = "13776120509"
        password = "aaasssddd"


        driver = webdriver.Chrome()
        # 获取登录的url
        driver.get(login_url)
        # time.sleep(5)
        driver.maximize_window()
        print "开始登录"

        # 获取登录用户名和密码的输入域
        name_field = driver.find_element_by_id('loginname')
        # name_field = driver.find_element_by_id('loginName')
        name_field.clear()
        name_field.send_keys(account)

        password_field = driver.find_element_by_name('password')
        # password_field = driver.find_element_by_id('loginPassword')
        password_field.clear()
        password_field.send_keys(password)

        # 提交

        submit = driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a/span')
        # submit = driver.find_element_by_xpath('//*[@id="loginAction"]')
        time.sleep(2)

        submit.click()
        time.sleep(5)

        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'WB_miniblog')))
        source = driver.page_source
        if(self.is_login(source)):
            print "登录成功"
        sina_cookie = driver.get_cookies()
        driver.quit()
        return sina_cookie

    def is_login(self,source):
        rs = re.search("CONFIG\['islogin'\]='(\d)'", source)
        if rs:
            return int(rs.group(1)) == 1
        else:
            return False


    # 抓取用户基本信息
    def getUserInfo(self,userid):
        url = "https://api.weibo.com/2/users/show.json"
        params = {
            'access_token': _ACCESS_TOKEN,
            'uid':userid
        }
        user = requests.get(url=url,params=params).json()
        return [user['id'],user['friends_count'],user['followers_count'],user['statuses_count'],user['favourites_count'],user['gender'],user['verified'],user['city']]

    # 抓取几个领域的用户id
    def getUserID(self):
        # 抓一万个
        _MAX_Number = 10000
        # 用户id结果集
        actors_ids = set()
        directors_ids = set()
        singers_ids = set()
        players_ids = set()

        actors = "https://s.weibo.com/user/%25E6%25BC%2594%25E5%2591%2598&page="
        directors = "https://s.weibo.com/user/%25E5%25AF%25BC%25E6%25BC%2594&page="
        singers = "https://s.weibo.com/user/%25E6%25AD%258C%25E6%2589%258B&page="
        players = "https://s.weibo.com/user/%25E8%25BF%2590%25E5%258A%25A8%25E5%2591%2598&page="

        # 获取演员ids
        # self.getUsersID(actors,"actor")
        self.getUsersID(directors,"director")
        self.getUsersID(singers,"singer")
        self.getUsersID(players,"player")

    # 解析cookie
    def ParseCookie(self,cookie):
        res = {}
        cookies = cookie.split(";")
        for cook in cookies:
            key,value = cook.split("=")
            res[key.lstrip().rstrip()] = value.lstrip().rstrip()
        return res

    # 抓取某个领域
    def getUsersID(self,url,category):

        # 添加请求头信息
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

        # cookie信息
        cookie = "SINAGLOBAL=4043605503975.1895.1479819188716; UM_distinctid=1621ef12ef35c9-010737f44f7c2d-3a75045d-1fa400-1621ef12ef45eb; _s_tentry=ent.ifeng.com; YF-V5-G0=b1e3c8e8ad37eca95b65a6759b3fc219; Apache=1879352856775.3337.1523458056359; ULV=1523458056368:63:1:1:1879352856775.3337.1523458056359:1522138879467; YF-Page-G0=ee5462a7ca7a278058fd1807a910bc74; YF-Ugrow-G0=b02489d329584fca03ad6347fc915997; login_sid_t=bbb9fec459ca99f483b3f769202275a0; cross_origin_proto=SSL; wb_cmtLike_6050650176=1; appkey=; WBtopGlobal_register_version=25c556e6eb9b606e; un=13776120509; UOR=baike.baidu.com,widget.weibo.com,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhWjTyGjFD-0cyZI7kC7IYg5JpX5K2hUgL.Foe4S0eEShM0Sh22dJLoI0YLxKBLBonL1h5LxK-L1hnL1hMLxK.L1heLB.x4ICH8Sb-4SEHWeFH8Sb-R1C-ReFH81FHFeF-4e05pe8Yf1K-t; ALF=1556193541; SSOLoginState=1524657542; SCF=An2pxqirryGJ7asCvq8npDbZpxwysghsp8yKuZvilRtrXWhLE8QIsNFIrhHrLh2GU3_rzXqedvRprbtuo3Manyo.; SUB=_2A2535B3XDeRhGeVH7FET9CnPzz2IHXVUkAgfrDV8PUNbmtBeLROtkW9NTv9QmIdYSwu2WvFT2kBQImASHC9oWVKD; SUHB=0u5hXxfkXeS32X; wvr=6"
        cookie = self.ParseCookie(cookie)

        # 初始化chrome浏览器引擎
        browser = webdriver.Chrome(chrome_options=options)

        # browser.add_cookie(cookie_dict=cookie)
        browser.get(url+str(1))

        # # 添加cookie
        for key in cookie.keys():
            temp = {}
            temp["name"] = key
            temp['value'] = cookie[key]
            browser.add_cookie(temp)

        # 抓一万个
        _MAX_Number = 10000
        # 用户id结果集
        ids = set()
        pre = len(ids)

        pagesid = 1

        while(len(ids) < _MAX_Number):
            browser.get(url + str(pagesid))

            # 获取页面源
            html = browser.page_source

            # 开始解析
            soup = BeautifulSoup(html)
            # 得到所有a标签,class属性为 W_texta W_fb
            res = soup.findAll('div',"fr followed")
            for r in res:
                try:
                    groups = re.match(r'uid=(\d+)&type=follow',r['action-data'])
                    ids.add(groups.group(1))
                except Exception as e:
                    pass
            print len(ids)
            pagesid += 1
            # 睡眠
            time.sleep(5)
            if len(ids) == pre:
                break
            else:
                pre = len(ids)

        browser.close()

        # 将结果持久化
        with open(category,'w') as f:
            pickle.dump(ids,f)
        return ids

    # 抓取某个用户关注的用户id
    def getUserFriends(self,userid):
        friends = set()
        return friends



if __name__ == '__main__':
    crawler = Crawler()
    # user = crawler.getUserInfo("1770438374")
    # print user
    crawler.getUserID()
    # crawler.login()