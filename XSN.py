#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import random
import networkx as nx
from networkx.classes.function import all_neighbors

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

    # 求邻居
    def N1(self,v,profiles):
        neighbours = set(all_neighbors(self.g,v))
        return neighbours - set(profiles)

    def N2(self,profiles):
        neighbours = reduce(lambda x,y:all_neighbors(self.g,x) | all_neighbors(self.g,y),profiles)
        return neighbours | set(profiles)

    def Search(self):
        profiles = set()
        # 随机加一个点进入
        profiles.add(random.randint(0,self.num))
        while len(profiles) < self.k:
            # 每次加入使得|N(v) - (N(S) | S)|最大的元素
            results = {i:len(self.N1(i,profiles) - self.N2(profiles)) for i in profiles if i not in profiles}
            to_add = max(results.items(),key=lambda key:key[1])[0]
            profiles.add(to_add)
        # 将profiles转换一下
        profiles = [self.id_list[i] for i in profiles]
        return profiles
