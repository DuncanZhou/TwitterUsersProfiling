#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import pickle
import numpy as np
import time
import networkx as nx
import Initial as init
import Metric

class PageRank:
    def __init__(self,users,features,R,k,id_list,g):
        # 返回top k个
        self.k = k
        # 用户数据
        self.users = users
        # 特征列
        self.features = features
        # 图结构
        self.g = g
        # 结点对应编号
        # 转换成字典,id_list中的id为string类型
        self.id_dic = dict(zip(id_list,range(len(id_list))))
        # 节点编号
        self.id_list = id_list
        # 评价标准
        self.metric = Metric.Metrics(users,features,R,id_list,g)

    def PR(self):
        start_time = time.time()
        pr = nx.pagerank(self.g,alpha=0.85)
        end_time = time.time()
        print "PageRank costs %f s" % (end_time - start_time)

        res = sorted(pr.items(),key=lambda key:key[1],reverse=True)[:self.k]
        profiles = [int(self.id_list[e[0]]) for e in res]
        print self.metric.RScore(profiles)
        return profiles

def test():
    category = "Religion"
    feature,users,R,id_list,g = init.Init(category)
    num = int(len(users) * 0.05)
    pagerank = PageRank(users,feature,R,num,id_list,g)
    pagerank.PR()

test()
