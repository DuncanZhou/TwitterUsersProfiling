#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import Metric as metric
import time
from copy import deepcopy
from numpy import *
import numpy as np
import pickle
import os

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
        # 最大的代表性
        self.max_repre = 0
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

    # 贪心寻找,暂不管领域典型条件
    def SearchWithoutConstraints(self):
        # 每次并入使得目标函数最小化
        profiles = set()
        people = datapre.People(self.features)
        print "数据集装载完毕"
        for category in self.categories.keys():
            # p_number为该领域需要的人数
            p_number = (int)(self.k * self.categories[category]) + 1
            # tuples为该领域所有的人
            tuples = people[category]

            if not os.path.exists("new%sRepresentativeMatrix.pickle.npy" % category):
                # 两重循环计算代表性矩阵
                R = []
                print len(tuples)
                for id in tuples:
                    row = []
                    for id1 in tuples:
                        row.append(metric.Repre(self.features[id],self.features[id1]))
                    R.append(row)
                # 将R持久化
                # save_file = open("%sRepresentativeMatrix.pickle" % category,"wb")
                # pickle.dump(R,save_file)
                # save_file.close()
                # 使用另一种保存方式
                R = np.asarray(R)
                np.save("new%sRepresentativeMatrix.pickle.npy" % category,R)
                # 将用户id在矩阵中对应的行保存
                R_dic = {}
                for id,i in zip(tuples,xrange(len(tuples))):
                    R_dic[id] = i
                save_file = open("new%sRepresentativeDictionary.pickle" % category,"wb")
                pickle.dump(R_dic,save_file)
                save_file.close()
            else:
                # 加载矩阵
                # open_file = open("%sRepresentativeMatrix.pickle" % category)
                # R = pickle.load(open_file)
                # open_file.close()
                # 换一种加载方式
                R = np.load("new%sRepresentativeMatrix.pickle.npy" % category)
            rowN = len(tuples)
            results_vector = np.asarray([0 for i in xrange(rowN)])
            # 得到了代表性矩阵后
            count = 0
            has = {}
            while count < p_number:
                # results = {i:sum(max(x,y) for x,y in zip(R[i],results_vector)) for i in xrange(rowN) if i not in has}
                results = {i:sum(np.max(np.vstack((R[i],results_vector)),axis=0)) for i in xrange(rowN) if i not in has}
                to_add = (max(results.items(),key=lambda key:key[1]))[0]
                has[to_add] = tuples[to_add]
                profiles.add(tuples[to_add])
                # 更新
                results_vector = np.max(np.vstack((R[to_add],results_vector)),axis=0)
                # results_vector = [max(x,y) for x,y in zip(R[to_add],results_vector)]
                count += 1
                print "the number of profiles is %d" % len(profiles)
        return list(profiles)

    # 删除多出来的用户
    def Delete(self,profiles):
        print "开始删除多余结点"
        # 先统计每个领域的人数,用以统计该领域是否能被减少人数
        categories = self.DomainDistribution(profiles)
        people = datapre.People(self.features)
        # 遍历,如果将其排除,那么损耗将会减少多少,将排除后损失依然小的排除
        to_delete = len(profiles) - self.k
        has_category = set()
        count = 0
        results = {}
        for category in categories.keys():
            if categories[category] == 1 or categories[category] == int(self.categories[category] * self.k):
                # 该领域不能删除
                continue
            profile_domain = set([id for id in profiles if self.features[id][5] == category])
            if os.path.exists("new%sRepresentativeMatrix.pickle.npy" % category):
                # 加载矩阵
                # open_file = open("%sRepresentativeMatrix.pickle" % category)
                # R = pickle.load(open_file)
                # open_file.close()
                R = np.load("new%sRepresentativeMatrix.pickle.npy" % category)
                # 加载id字典
                open_file = open("%sRepresentativeDictionary.pickle" % category)
                R_dic = pickle.load(open_file)
                open_file.close()
                # 该领域的代表性人物对应的所有行
                rows = set([R_dic[id] for id in profile_domain])
                original = sum(np.max(np.asarray([R[i] for i in rows]),axis=0))
                subresults = {profile:(original - sum(np.max(np.asarray([R[i] for i in (rows - {R_dic[profile]})]),axis=0))) for profile in profile_domain}

                to_delete_id = (min(subresults.items(),key=lambda key:key[1]))[0]
                results[to_delete_id] = subresults[to_delete_id]
        # print len(results)
        results = sorted(results.items(),key=lambda key:key[1])
        for result in results:
            profiles.remove(result[0])
            print "the number of profiles is %d" % len(profiles)
            has_category.add(self.features[result[0]][5])
            count += 1
            if count == to_delete:
                break
        return profiles

    # 贪心算法保证k个情况
    # def SearchWithK(self):
    #     people = datapre.People()
    #     profiles = set()
    #     has_category = set()
    #     category_loss = {}
    #     count = 0
    #     while count < self.k:
    #         results = {}
    #         for category in self.categories.keys():
    #             if category in has_category:
    #                 continue
    #             result = {}
    #             # tuples为该领域所有的人
    #             tuples = people[category]
    #             for id in tuples:
    #                 if id not in profiles:
    #                     profiles.add(id)
    #                     if category not in category_loss.keys():
    #                         result[id] = -metric.AttributeLossByDomain(self.features, profiles,category)
    #                     else:
    #                         result[id] = metric.AttributeLossByDomain(self.features,profiles,category) - category_loss[category]
    #                     profiles.remove(id)
    #             results[(min(result.items(),key=lambda key:key[1]))[0]] = (min(result.items(),key=lambda key:key[1]))[1]
    #
    #         to_add = (min(results.items(),key=lambda key:key[1]))[0]
    #         # print self.features[to_add][5]
    #         # 检查该领域有没有超出人数限制
    #         number = 0
    #         category = self.features[to_add][5]
    #         for profile in profiles:
    #             if self.features[profile][5] == category:
    #                 number += 1
    #         if number < ((int)(self.k * self.categories[category]) + 1):
    #             # 可以加入
    #             profiles.add(to_add)
    #             print self.features[to_add][5]
    #             category_loss[category] = metric.AttributeLossByDomain(self.features,profiles,category)
    #             count += 1
    #         else:
    #             # 该领域不能再加入元素了
    #             has_category.add(self.features[to_add][5])
    #         # print count
    #     return profiles

    # 对非典型的元素进行替换
    def Replace(self,target,profiles):
        # people为每个领域的用户集合
        people = datapre.People(self.features)
        category = self.features[target][5]

        index = profiles.index(target)
        old_element = profiles[index]

        profile_domain = set([id for id in profiles if self.features[id][5] == category])

        if os.path.exists("new%sRepresentativeMatrix.pickle.npy" % category):
            # 加载矩阵
            # open_file = open("%sRepresentativeMatrix.pickle" % category)
            # R = pickle.load(open_file)
            # open_file.close()
            R = np.load("new%sRepresentativeMatrix.pickle.npy" % category)
            # 加载id字典
            open_file = open("%sRepresentativeDictionary.pickle" % category)
            R_dic = pickle.load(open_file)
            open_file.close()
            # 该领域的代表性人物对应的所有行
            rows = set([R_dic[id] for id in profile_domain])
            results = {element:sum(np.max(np.asarray([R[i] for i in rows | {R_dic[element]}]),axis=0)) for element in people[category] if element not in set(profiles)}
            results = sorted(results.items(),key=lambda dic:dic[1],reverse=True)
            for result in results:
                to_replace = result[0]

                if metric.checkOneTypical(to_replace,profiles,self.epsilon):
                    self.replace[target] = to_replace
                    profiles[index] = old_element
                    # print new_element
                    return to_replace
        return None

        # # 对target进行替换(在其所属领域寻找满足领域典型的,同样使用贪心算法)
        # index = profiles.index(target)
        # old_element = profiles[index]
        # results = {}
        # for person in people[self.features[target][5]]:
        #     if person != target and person not in profiles and metric.checkOneTypical(person,profiles,self.epsilon):
        #         profiles[index] = person
        #         results[person] = metric.AttributeRepresentativeByDomain(set(profiles),self.features[target][5])
        # new_element = (max(results.items(),key=lambda key:key[1]))[0]
        # self.replace[target] = new_element
        # profiles[index] = old_element
        # # print new_element
        # return new_element

    # 在边集合中删除与点相关的边
    @staticmethod
    def DeleteEdges(edges,vertex):
        newedges = deepcopy(edges)
        for edge in edges:
            if edge[0] == vertex:
                newedges.remove(edge)
        return newedges

    # 检查在边集合中还是否有与vertex相连的边
    @staticmethod
    def CheckEdgeCase1(edges,vertex):
        for edge in edges:
            if edge[1] == vertex or edge[0] == vertex:
                return False
        return True

    # 检查是否有其他元素与其相连着
    @staticmethod
    def CheckEdgeCase2(edges,vertex):
        for edge in edges:
            if edge[1] == vertex:
                # 有相连
                return True
        return False

    # 统计集合中每个领域相应的人数
    def DomainDistribution(self,profiles):
        categories = datapre.DomainDistribution(profiles,self.features)
        return categories

    # 递归替换非领域典型元素算法
    def SearchRecursion(self,index,current_profiles,noneTypical,edges):
        # 递归终止条件(已经)
        if metric.checkAllTypical(current_profiles,self.epsilon):
            # print "找到一个可行解"
            temp = metric.AttributeRepresentative(set(current_profiles))
            if self.max_repre == 0 or temp > self.max_repre:
                self.max_repre = temp
                self.best_profiles = set(current_profiles)
                # print self.best_profiles
                print self.max_repre
            return
        # 不是典型,而最小的损耗已经大于最小损耗,不必再向下搜索了
        if index == len(noneTypical):
            return

        # 三种情况,不替换,替换,可替换可不替换

        i = noneTypical[index]
        # 第一种情况
        if self.CheckEdgeCase1(edges,i) == True:
            # 不替换
            self.SearchRecursion(index + 1,current_profiles,noneTypical,edges)

        elif self.CheckEdgeCase2(edges,i) == True:
            # 替换
            new_profiles = deepcopy(current_profiles)
            # 先在已经计算过的字典中去寻找
            if current_profiles[i] in self.replace.keys() and metric.checkOneTypical(current_profiles[i],new_profiles,self.epsilon):
                new_profiles[i] = self.replace[current_profiles[i]]
            else:
                if self.Replace(current_profiles[i],new_profiles) == None:
                    print "不可替换"
                    return
                new_profiles[i] = self.Replace(current_profiles[i],new_profiles)

            # 删除edges中与i相关的边
            newedges = self.DeleteEdges(edges,i)
            # 替换后继续向下寻找
            self.SearchRecursion(index + 1,new_profiles,noneTypical,newedges)
        else:
            # 替换或不替换
            # 替换
            new_profiles = deepcopy(current_profiles)
            # 先在已经计算过的字典中去寻找
            if current_profiles[i] in self.replace.keys() and metric.checkOneTypical(current_profiles[i],new_profiles,self.epsilon):
                new_profiles[i] = self.replace[current_profiles[i]]
            else:
                if self.Replace(current_profiles[i],new_profiles) == None:
                    print "不可替换"
                    return
                new_profiles[i] = self.Replace(current_profiles[i],new_profiles)

            # 删除edges中与i相关的边
            newedges = self.DeleteEdges(edges,i)
            # print len(newedges)
            # 替换后继续向下寻找
            self.SearchRecursion(index + 1,new_profiles,noneTypical,newedges)
            # 不替换继续向下寻找
            self.SearchRecursion(index + 1,current_profiles,noneTypical,edges)
        return

    # 先不管典型贪心寻找,然后在进行替换寻找最优值
    def SearchWithReplace(self):
        # 第一步,在没有领域典型的条件得到的贪心最优值
        current_profiles = self.SearchWithoutConstraints()
        print metric.AttributeRepresentative(set(current_profiles))
        # 持久化找到的代表性人物
        # with open("%dGBProfiles" % len(current_profiles),"wb") as f:
        #     for profile in current_profiles:
        #         f.write(profile)
        #         f.write("\n")
        # self.best_profiles = self.SearchWithK()
        # print metric.AttributeLoss(self.features,self.best_profiles)

        # 贪心排除多余的
        self.best_profiles = self.Delete(set(current_profiles))

        # 统计一下每个领域的人数
        # categories = self.DomainDistribution(self.best_profiles)

        # 第二步,排除不够典型的,统计贪心算法求得的解中有哪些不够典型的
        # 将best_profiles中不够典型的元素求出
        best_profiles = list(self.best_profiles)
        # 直接贪心搜索到的解的损耗是
        print "直接贪心搜索到的解的属性代表性是"
        print metric.AttributeRepresentative(self.best_profiles)
        # vertexs = set()
        # # 顶点替换代价
        # vertexs_cost = {}
        # 不够典型的点的编号
        NoneTypical = []
        edges = []
        i = 0
        while i < len(best_profiles):
            j = i + 1
            while j < len(best_profiles):
                if metric.Similarity(best_profiles[i],best_profiles[j]) > self.epsilon:
                    edges.append((i,j))
                j += 1
            i += 1
        for profile in best_profiles:
            if not metric.checkOneTypical(profile,self.best_profiles,self.epsilon):
                NoneTypical.append(best_profiles.index(profile))
        print NoneTypical

        print "开始替换不够领域典型的人物"
        self.SearchRecursion(0,best_profiles,list(NoneTypical),edges)

        return self.best_profiles

def test():

    to_run = [40,60,80,100]
    for i in to_run:
        start_time = time.time()
        method = Greedy(i,datapre.Features(),datapre.CategoriesDistribution(),0.1555)
        # profiles = method.SearchWithoutConstraints()
        # profiles = method.SearchWithConstraints()
        profiles = method.SearchWithReplace()
        # print len(profiles)
        end_time = time.time()

        # 将结果写入文件
        with open("%dGB_results" % i,"wb") as f:
            f.write("cost %f s" % (end_time - start_time))
            f.write("\n")
            f.write("Attribute Representativeness is:")
            f.write(str(metric.AttributeRepresentative(profiles)))
            f.write("\n")
            for profile in profiles:
                f.write(profile + "\t")
test()