#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import math
import random
import Distance as dist
import Metric as metric
import GreedyAlgorithm as greedy
import Queue
import copy

class SAalgo:
    def __init__(self,k,features,categories,epsilon,neighbour,init_temper,dec):
        # 初始温度init_temper,温度下降参数delta
        self.temper = init_temper
        self.dec = dec
        # 需要找寻的代表性子集的大小
        self.k = k
        # 全局特征向量集
        self.features = features
        # 人物领域分布
        self.categories = categories
        # 领域典型的阈值
        self.epsilon = epsilon
        # 定义领域范围值
        self.neighbour = neighbour

    # accept函数
    @staticmethod
    def accept(delta,temper):
        if delta < 0:
            return True
        else:
            print math.exp(-delta * 1.0 / temper)
            return math.exp(-delta * 1.0 / temper) > random.random()
            # return False

    def Search(self):
        # 将人物按领域分类
        people = {}
        for key in self.features.keys():
            if self.features[key][5] not in people.keys():
                people[self.features[key][5]] = [key]
            else:
                people[self.features[key][5]].append(key)

        # 初始解(贪心算法获得)
        method = greedy.Greedy(self.k,self.features,self.categories,self.epsilon)
        current_profiles = set(method.Search())

        while self.temper > 1.1:
            change = False
            # 开始迭代搜索解,对于领域解S,如果S优于当前解则接受领域解,否则以一定概率接受(如此避免了局部最优)
            for profile in current_profiles:
                # 对其中每个元素的领域元素判断,将profile领域的元素加入队列中
                neighbours = Queue.Queue()
                tuples = people[self.features[profile][5]]
                for id in tuples:
                    if id not in current_profiles and dist.distance(self.features[id],self.features[profile]) <= self.neighbour:
                        neighbours.put(id)
                print "有%d个邻居" % neighbours.qsize()
                new_profiles = copy.deepcopy(current_profiles)
                new_profiles.remove(profile)
                # 对其领域进行判断
                while not neighbours.empty():
                    to_check = neighbours.get()
                    old_loss = metric.AttributeLoss(self.features,current_profiles)
                    new_profiles.add(to_check)
                    new_loss = metric.AttributeLoss(self.features,new_profiles)
                    delta = new_loss - old_loss
                    # print old_loss
                    # print new_loss
                    flag = self.accept(delta,self.temper)
                    if flag and metric.checkOneTypical(self.features,to_check,new_profiles,self.epsilon):
                        current_profiles = new_profiles
                        change = True
                        break
                    new_profiles.remove(to_check)
            if not change:
                # 没有改变
                break
            self.temper *= self.dec
        return list(current_profiles)

def test():
    method = SAalgo(20,datapre.Features(),datapre.CategoriesDistribution(),0.05,0.5,10,0.9)
    profiles = method.Search()
    print "Attribute Loss is"
    print metric.AttributeLoss(method.features,profiles)
test()