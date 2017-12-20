#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import math
import random
import Metric as metric
import pandas as pd
import cPickle as pickle
import networkx as nx
import time
import numpy as np

class SAalgo:
    def __init__(self,k,init_temper,dec,users,feature,R,id_list,g):
        # 初始温度init_temper,温度下降参数delta
        self.temper = init_temper
        self.dec = dec
        # 需要找寻的代表性子集的大小
        self.k = k
        # 加载用户数据
        self.users = users
        # 加载评价类
        self.metric = metric.Metrics(users,feature,R,id_list,g)

    # accept函数
    @staticmethod
    def accept(delta,temper):
        if delta > 0:
            return True
        else:
            return math.exp(delta * 1.0 / temper) > random.random()

    def Search(self):
        # profiles初始化,任选k个加入
        ids = random.sample(range(len(self.users)),self.k)
        seeds = [self.users.loc[id]['userid'] for id in ids]
        profiles = set(seeds)
        best_profiles = profiles.copy()
        cur_rscore = self.metric.RScore(best_profiles)
        best_rscore = cur_rscore
        # 从profiles中的邻居中挑选
        # neighbours = self.metric.GetNeighbours(seed)
        while self.temper > 1.1:
            change = False
            # 对当前profiles中的每个元素进行查找并替换,如果S优于当前解则接受领域解,否则以一定概率接受(如此避免了局部最优)
            for seed in profiles:
                neighbours = self.metric.GetNeighbours(seed) - profiles
                if len(neighbours) == 0:
                    continue
                # 从neighbours中随机选择一个加入
                choose = random.sample(neighbours,1)[0]
                # 用choose替换seed,如果结果优于当前,则接受,否则以概率接受
                profiles.remove(seed)
                profiles.add(choose)
                new_rscore = self.metric.RScore(profiles)
                delta = new_rscore - cur_rscore
                if self.accept(delta,self.temper) == False:
                    profiles.remove(choose)
                    profiles.add(seed)
                else:
                    change = True
                    # 保留最优值
                    if new_rscore > best_rscore:
                        best_profiles = profiles.copy()
                        best_rscore = new_rscore
            if not change:
                # 没有改变
                break
            self.temper *= self.dec
        print best_rscore
        return list(best_profiles)

def test():
    # 加载数据
    print "加载数据"
    category = "Religion"
    feature = ['followers','friends','statuses','favourites','activity','influence','location','verified']
    id_list_path = "%s_ids" % category
    rels_path = "%s_rels" % category
    users = pd.read_csv(category+"Users.csv")
    R = np.load("%sRepresentativeMatrix.npy" % category)
    ids_file = open(id_list_path,'rb')
    id_list = pickle.load(ids_file)
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    g = nx.Graph()
    g.add_edges_from(rels)
    print "数据加载完毕"
    ksa = SAalgo(int(len(users) * 0.01),10,0.9,users,feature,R,id_list,g)
    ksa.Search()
test()