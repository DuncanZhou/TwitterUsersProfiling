#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import random
import Initial as init
from networkx.classes.function import all_neighbors
import Metric
import time

class XSN:
    def __init__(self,k,id_list,g):
        # 采样个数
        self.k = k
        # 总人数
        self.num = len(id_list)
        # 图结构
        self.g = g
        # 结点编号
        self.id_list = id_list

    # def Neighbours(self,i):
    #     if i in self.g:
    #         return set(all_neighbors(self.g,i))
    #     else:
    #         return set()

    def Search(self):
        profiles = set()
        # 随机加一个点进入
        # seed = random.randint(0,self.num)
        # 加入相邻最多的一个点进来
        seed = random.choice(self.id_list)
        # results = {i:len(set(all_neighbors(self.g,str(i)))) for i in self.id_list if i in self.g}
        # seed = max(results.items(),key=lambda key:key[1])[0]
        # neighbours = set([i for i in self.Neighbours(seed)])
        neighbours = set([i for i in (all_neighbors(self.g,str(seed)) if str(seed) in self.g else set())])
        profiles.add(seed)
        neighbours.add(seed)
        while len(profiles) < self.k:
            # 每次加入使得|N(v) - (N(S) | S)|最大的元素
            # results = {i:len(set((all_neighbors(self.g,i) if i in self.g else set())) - profiles - neighbours ) for i in range(self.num) if i not in profiles}
            results = {i:len(set((all_neighbors(self.g,str(i)) if str(i) in self.g else set())) - profiles - neighbours ) for i in self.id_list if i not in profiles}
            to_add = max(results.items(),key=lambda key:key[1])[0]
            profiles.add(to_add)
            # 更新neighbours
            neighbours |= set([i for i in (all_neighbors(self.g,to_add) if to_add in self.g else set())])
            neighbours.add(to_add)
            # print len(profiles)
        profiles = [int(i) for i in profiles]
        return profiles

def test():
    category = "Actor"
    users,R,id_list,g = init.Init(category)
    metric = Metric.Metrics(users,R,id_list,g)
    num = len(users) * 0.15
    xsn = XSN(num,id_list,g)
    start_time = time.time()
    profiles = xsn.Search()
    end_time = time.time()
    rc,rt,r_score = metric.RScore(profiles)
    print "cost %f s" % (end_time - start_time)
    print "rc:%f,rt:%f,r_score:%f" % (rc,rt,r_score)
test()
