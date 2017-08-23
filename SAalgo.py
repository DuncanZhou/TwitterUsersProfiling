#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import math
import random
import Distance as dist
import Metric as metric
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
        if delta > 0:
            return True
        else:
            print math.exp(delta * 1.0 / temper)
            return math.exp(delta * 1.0 / temper) > random.random()
            # return False

    # 删除多出来的用户
    def Delete(self,profiles):
        # 先统计每个领域的人数,用以统计该领域是否能被减少人数
        categories = datapre.DomainDistribution(profiles,self.features)
        # 遍历,如果将其排除,那么损耗将会减少多少,将排除后损失依然小的排除
        to_delete = len(profiles) - self.k
        has_category = set()
        i = 0
        while i < to_delete:
            repre = {}
            for profile in profiles:
                if self.features[profile][5] in has_category:
                    continue
                profiles.remove(profile)
                repre[profile] = metric.AttributeRepresentative(self.features,profiles)
                profiles.add(profile)
            # 对loss排个序,把代表性依然大的且可以移除的移除
            to_delete_id = (max(repre.items(),key=lambda dic:dic[1]))[0]
            has_category.add(self.features[to_delete_id][5])
            # 判断是否能删除
            if categories[self.features[to_delete_id][5]] == int(self.categories[self.features[to_delete_id][5]] * self.k) + 1:
                profiles.remove(to_delete_id)
                i += 1
        return profiles

    # 退火算法初始解由随机产生或者贪心产生
    def Greedy(self):
        people = datapre.People(self.features)
        # 每次并入使得目标函数最小化
        profiles = set()
        for category in self.categories.keys():
            # p_number为该领域需要的人数
            p_number = int(self.k * self.categories[category]) + 1
            # tuples为该领域所有的人
            tuples = people[category]
            # 迭代p_number次
            count = 0
            has_checked = set()
            while count < p_number:
                results = {}
                for id in tuples:
                    if id not in has_checked:
                        profiles.add(id)
                        results[id] = metric.AttributeRepresentativeByDomain(self.features,list(profiles),category)
                        profiles.remove(id)
                # 将最小的id加入到profiles中
                to_add = (max(results.items(),key=lambda key:key[1]))[0]
                has_checked.add(to_add)
                # 检查是否领域典型约束
                flag = metric.checkOneTypical(self.features,to_add,profiles,self.epsilon)
                if flag:
                    profiles.add(to_add)
                    count += 1
                else:
                    # print "拒绝"
                    pass

        # 删除多出来的用户
        if len(profiles) > self.k:
            profiles = self.Delete(profiles)
        # print len(profiles)
        return profiles

    def Search(self):
        # 将人物按领域分类
        people = datapre.People(self.features)

        # 初始解(贪心算法获得)
        current_profiles = self.Greedy()

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
                    old_loss = metric.AttributeRepresentative(self.features,current_profiles)
                    new_profiles.add(to_check)
                    new_loss = metric.AttributeRepresentative(self.features,new_profiles)
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
    print metric.AttributeRepresentative(method.features,profiles)
test()