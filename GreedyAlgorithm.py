#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import Metric as metric
import time
import copy

class Greedy:
    def __init__(self,k,features,categories,epsilon):
        '''

        :param k: 共计需要寻找的代表性子集大小
        :param categories: 领域分布
        :param features: 全局特征集
        '''
        self.k = k
        self.features = features
        # 全局领域分布情况
        self.categories = categories
        # 典型性判断参数
        self.epsilon = epsilon
        # 最优代表性子集
        self.best_profiles = set()
        # 最小的损耗
        self.min_loss = 0
        # 记录每个领域内按照目标函数值从小到大排序
        self.replace = {}

    # 将一个领域内的用户按距离排序
    @staticmethod
    def SortByDistance(ids,features):
        id_dist = {}
        for id1 in ids:
            distance = 0
            for id2 in ids:
                distance += dist.distance(features[id1],features[id2])
            id_dist[id1] = distance

        # 对字典进行排序
        id_dists = sorted(id_dist.items(),key=lambda key:key[1])
        return id_dists

    # 将人物按领域分类
    def People(self):
        # 将人物按领域分类
        people = {}
        for key in self.features.keys():
            if self.features[key][5] not in people.keys():
                people[self.features[key][5]] = [key]
            else:
                people[self.features[key][5]].append(key)
        return people

    # 贪心寻找,暂不管领域典型条件
    def SearchWithoutConstraints(self):
        # 每次并入使得目标函数最小化
        profiles = set()
        for category in self.categories.keys():
            # p_number为该领域需要的人数
            p_number = (int)(self.k * self.categories[category]) + 1
            # tuples为该领域所有的人
            tuples = [id for id in self.features.keys() if self.features[id][5] == category]
            # 迭代p_number次
            count = 0
            while count < p_number:
                results = {}
                for id in tuples:
                    if id not in profiles:
                        profiles.add(id)
                        results[id] = metric.AttributeLossByDomain(self.features,list(profiles),category)
                        profiles.remove(id)
                # 将最小的id加入到profiles中
                to_add = (min(results.items(),key=lambda key:key[1]))[0]
                profiles.add(to_add)
                count += 1
        # print len(profiles)
        return list(profiles)

    # 对非典型的元素进行替换
    def Replace(self,target,profiles):
        # people为每个领域的用户集合
        people = self.People()
        # 对target进行替换(在其所属领域寻找满足领域典型的,同样使用贪心算法)
        index = profiles.index(target)
        results = {}
        for person in people[self.features[target][5]]:
            if person != target and person not in profiles and metric.checkOneTypical(self.features,person,profiles,self.epsilon):
                profiles[index] = person
                results[person] = metric.AttributeLossByDomain(self.features,set(profiles),self.features[target][5])
        new_element = (min(results.items(),key=lambda key:key[1]))[0]
        self.replace[target] = new_element
        # print new_element
        return new_element

    # 递归替换非领域典型元素算法
    def SearchRecursion(self,start,current_profiles):
        i = start
        while i < len(current_profiles):
            old_element = current_profiles[i]
            # print old_element
            # 如果非典型就替换该元素
            if not metric.checkOneTypical(self.features,current_profiles[i],set(current_profiles),self.epsilon):
                # 先在已经计算过的字典中去寻找
                if current_profiles[i] in self.replace.keys():
                    current_profiles[i] = self.replace[current_profiles[i]]
                    if not metric.checkOneTypical(self.features,current_profiles[i],current_profiles,self.epsilon):
                        # 重新寻找,替换这一步比较慢
                        current_profiles[i] = self.Replace(current_profiles[i],current_profiles)
                else:
                    current_profiles[i] = self.Replace(current_profiles[i],current_profiles)
                # print "第%d个元素,旧的元素为:" % i
                # print old_element
                # print "新的元素为:"
                # print current_profiles[i]
            if metric.checkAllTypical(self.features,current_profiles,self.epsilon):
                # print "找到一个可行解"
                if self.min_loss == 0 or metric.AttributeLoss(self.features,set(current_profiles)) < self.min_loss:
                    self.min_loss = metric.AttributeLoss(self.features,set(current_profiles))
                    self.best_profiles = set(current_profiles)
                return
            #
            # print current_profiles
            # 继续向下寻找
            self.SearchRecursion(i + 1,current_profiles)
            # print self.min_loss
            # 如果被替换了,还替换回来
            current_profiles[i] = old_element
            # 继续搜索
            i += 1
            print self.min_loss
        return


    # 删除多出来的用户
    def Delete(self,profiles):
        # 遍历,如果将其排除,那么损耗将会多少,将排除后损失依然小的排除
        to_delete = len(profiles) - self.k
        i = 0
        while i < to_delete:
            loss = {}
            for profile in profiles:
                profiles.remove(profile)
                loss[profile] = metric.AttributeLoss(self.features,profiles)
                profiles.add(profile)
            # 对loss排个序,把损耗依然小的可以移除
            to_delete_id = (min(loss.items(),key=lambda dic:dic[1]))[0]
            profiles.remove(to_delete_id)
            i += 1
        return profiles

    # 先不管典型贪心寻找,然后在进行替换寻找最优值
    def SearchWithReplace(self):
        # 第一步,在没有领域典型的条件得到的贪心最优值
        current_profiles = self.SearchWithoutConstraints()

        # 贪心排除多余的
        self.best_profiles = self.Delete(set(current_profiles))

        # 第二步,排除不够典型的,统计贪心算法求得的解中有哪些不够典型的

        self.SearchRecursion(0,list(self.best_profiles))

        return self.best_profiles

    # 贪心寻找(考虑了领域典型条件,边贪心寻找,边判断条件)
    def SearchWithConstraints(self):
        # 每次并入使得目标函数最小化
        profiles = set()
        for category in self.categories.keys():
            # p_number为该领域需要的人数
            p_number = (int)(self.k * self.categories[category]) + 1
            # tuples为该领域所有的人
            tuples = [id for id in self.features.keys() if self.features[id][5] == category]
            # 迭代p_number次
            count = 0
            has_checked = set()
            while count < p_number:
                results = {}
                for id in tuples:
                    if id not in has_checked:
                        profiles.add(id)
                        results[id] = metric.AttributeLossByDomain(self.features,list(profiles),category)
                        profiles.remove(id)
                # 将最小的id加入到profiles中
                to_add = (min(results.items(),key=lambda key:key[1]))[0]
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
        return list(profiles)

def test():
    start_time = time.time()
    method = Greedy(30,datapre.Features(),datapre.CategoriesDistribution(),0.0499)
    # profiles = method.SearchWithoutConstraints()
    # profiles = method.SearchWithConstraints()
    profiles = method.SearchWithReplace()
    # print len(profiles)
    end_time = time.time()
    print "cost %f s" % (end_time - start_time)
    print "Attribute Loss is"
    print metric.AttributeLoss(method.features,profiles)

test()




