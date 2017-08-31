#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# k-mediods,是k-means的一种变体.相较于k-means他不再是简单地选取一个均值作为聚类簇的质点,而是
# 寻找在聚类簇中距离之差之和最小的作为最新质点.同时,因为这样,该算法的复杂度高于k-means

import DataPrepare as datapre
import Distance as dist
import Metric as metric
from copy import deepcopy
import time
import pickle
import os
import numpy as np

class KMedoidsCluster:
    def __init__(self,k,datasets,category):
        # 需要聚类的数据集合
        self.features = datasets
        # 定义最大迭代次数
        self.Max_iteration = 30
        # 定义聚类簇个数
        self.k_min = k

        #
        self.R = np.load("new%sRepresentativeMatrix.pickle.npy" % category)
        # 加载id字典
        open_file = open("%sRepresentativeDictionary.pickle" % category)
        self.R_dic = pickle.load(open_file)
        open_file.close()

    # 计算质点到其聚类簇中其它点的代表性之和
    def CalcRepre(self,clusters,point):
        '''

        :param cluster: cluster为聚类簇,为list类型
        :param point: 质点
        :return:
        '''

        return sum(np.asarray([self.R[self.R_dic[point]][self.R_dic[col]] for col in clusters]))
        # sum = 0
        # for seed in clusters:
        #     sum += metric.Repre(self.features[seed],self.features[point])
        # return sum

    # 选取新的质点,代表性最大的作为新的质点
    def SelectNewMediod(self,clusters):
        results = {element:self.CalcRepre(clusters,element) for element in clusters}
        return (max(results.items(),key=lambda key:key[1]))[0]

    # 聚类
    def Cluster(self):
        k = self.k_min
        # 初始化种子
        k_seeds = list(datapre.Initial(self.features,k))
        # 聚类领域
        # 聚类簇
        cluster = {}

        # 开始迭代
        iteration = 0
        while iteration < self.Max_iteration:
            print k_seeds
            for seed in k_seeds:
                cluster[seed] = set()

            # 对所有元素进行聚类
            for key in self.features.keys():
                results = {seed:self.R[self.R_dic[seed],self.R_dic[key]] for seed in k_seeds}
                # results = {}
                # for seed in k_seeds:
                #     results[seed] = metric.Repre(self.features[seed],self.features[key])
                # 距离k_seeds中的id最近,并入id聚类簇中
                id = (max(results.items(),key=lambda key:key[1]))[0]
                # 并入该聚类簇中
                cluster[id] = cluster[id] | {key}
            print "新的聚类簇形成"
            # for seed in k_seeds:
            #     print len(cluster[seed])
            # 更新质点向量
            # flag来判断是否需要停止迭代
            flag = True
            # 对每个聚类簇分别判断
            print "更新聚类中心"
            new_k_seeds = set()
            for seed in k_seeds:
                new_mediod = self.SelectNewMediod(list(cluster[seed]))
                new_k_seeds.add(new_mediod)
                if new_mediod != seed:
                    # 需要继续迭代
                    flag = False

            if flag == True:
                # 停止迭代
                break
            k_seeds = new_k_seeds
            iteration += 1
            print "迭代%d次" % iteration

        return cluster,k_seeds

class KMedoids:
    # 初始函数
    def __init__(self,k,categories,epsilon):
        self.features = datapre.Features()
        # 一共需要人数
        self.k = k
        # 全局领域分布情况
        self.categories = categories
        # 典型性判断参数
        self.epsilon = epsilon

        # 统计集合中每个领域相应的人数
    def DomainDistribution(self,profiles):
        categories = datapre.DomainDistribution(profiles,self.features)
        return categories

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
                # open_file = open("%sRepresentativeMatrix.pickle.npy" % category)
                # R = pickle.load(open_file)
                # open_file.close()
                R = np.load("%sRepresentativeMatrix.pickle.npy" % category)
                # 加载id字典
                open_file = open("%sRepresentativeDictionary.pickle" % category)
                R_dic = pickle.load(open_file)
                open_file.close()
                # 该领域的代表性人物对应的所有行
                rows = set([R_dic[id] for id in profile_domain])
                print len(rows)
                original = sum(np.max(np.asarray([R[i] for i in rows]),axis=0))
                print len(profile_domain)
                subresults = {profile:(original - sum(np.max(np.asarray([R[i] for i in (rows - {R_dic[profile]})]),axis=0))) for profile in profile_domain}

                to_delete_id = (min(subresults.items(),key=lambda key:key[1]))[0]
                print to_delete_id
                results[to_delete_id] = subresults[to_delete_id]
        # print len(results)
        results = sorted(results.items(),key=lambda key:key[1])
        for result in results:
            print "the number of profiles is %d" % len(profiles)
            profiles.remove(result[0])
            has_category.add(self.features[result[0]][5])
            count += 1
            if count == to_delete:
                break
        return profiles

    # 从聚类好的聚类簇中替换不满足要求的元素
    def Replace(self,profiles,cluster):
        '''

        :param profiles: 完成的中心点
        :param cluster: 字典形式的,以profiles为key,聚类簇value为列表格式
        :return: 返回替换好的profiles
        '''
        iteration = True
        # 替换过程用离medoids最近的且满足要求的元素来替换

        while True:
            new_profiles = deepcopy(profiles)
            for profile in profiles:
                if not metric.checkOneTypical(profile,new_profiles,self.epsilon):
                    new_profiles.remove(profile)
                    # 对profile进行替换,在cluster[profile]寻找profile对其代表性最大的元素,且满足条件的来替换
                    R = np.load("%sRepresentativeMatrix.pickle.npy" % self.features[profile][5])
                    # 加载id字典
                    open_file = open("%sRepresentativeDictionary.pickle" % self.features[profile][5])
                    R_dic = pickle.load(open_file)
                    open_file.close()

                    # 在其聚类簇中寻找到其代表性最大的来替换

                    results = {id:R[R_dic[id]][R_dic[profile]] for id in cluster[profile]}
                    # results = {element:metric.Repre(self.features[profile],self.features[element]) for element in cluster[profile]}
                    results = sorted(results.items(),key=lambda key:key[1],reverse=True)
                    flag = False
                    # 在results中找到profile最能代表的,且满足领域典型要求的元素
                    for result in results:
                        key = result[0]
                        if metric.checkOneTypical(key,new_profiles,self.epsilon):
                            new_profiles.add(key)
                            cluster[key] = cluster[profile]
                            cluster.pop(profile)
                            flag = True
                            break
                    # 没找到领域典型的,需要在该领域的原集中去除这部分元素,重新聚类
                    if flag == False:
                        iteration = False
                        # 对该领域去除这部分元素后,重新寻找k个聚类簇
                        category = self.features[profiles][5]
                        for profile in profiles:
                            if self.features[profile][5] == category:
                                new_profiles.remove(profile)
                        # 获取该领域的人物集合
                        tuples = datapre.People(self.features)[category]
                        # 去除cluster[profile]这部分元素
                        for element in tuples:
                            if element in set(cluster[profile]):
                                tuples.remove(element)
                        number = 0
                        for profile in profiles:
                            if self.features[profile][5] == category:
                                number += 1
                        # 重新对tuples聚类
                        method = KMedoidsCluster(number,datapre.FeaturesById(tuples,self.features))
                        clusters,medoids = method.Cluster()
                        for key in clusters.keys():
                            cluster[key] = clusters[key]
                        for element in medoids:
                            new_profiles.add(element)
                        # 此时new_profiles是最新的,继续向下替换

            if iteration == True:
                break
            else:
                profiles = new_profiles

        return new_profiles

    # 聚类结束
    def Search(self):
        profiles = set()
        medoids_clusters = {}
        # 对每个领域聚类
        people = datapre.People(self.features)
        for category in self.categories.keys():
            # 对每个领域进行聚类
            number = int(self.k * self.categories[category]) + 1
            tuples = people[category]
            method = KMedoidsCluster(number,datapre.FeaturesById(tuples,self.features),category)
            clusters,medoids = method.Cluster()
            # 先加入到profiles中
            for medoid in medoids:
                profiles.add(medoid)
                medoids_clusters[medoid] = clusters[medoid]
        print "开始删除"
        # 删除多出来的
        profiles = self.Delete(profiles)
        print "开始替换"
        profiles = self.Replace(profiles,medoids_clusters)
        return profiles



def test():
    to_run = [40,60,80,100]
    for i in to_run:
        start_time = time.time()
        method = KMedoids(i,datapre.CategoriesDistribution(),0.1556)
        profiles = method.Search()
        end_time = time.time()
        print metric.AttributeRepresentative(profiles)
        print profiles
        print "cost %f s" % (end_time - start_time)
        with open("%dclustering_result" % i,"wb") as f:
            f.write("cost %f s" % (end_time - start_time))
            f.write("\n")
            f.write("Attribute Representativeness is:")
            f.write(str(metric.AttributeRepresentative(profiles)))
            f.write("\n")
            for profile in profiles:
                f.write(profile + "\t")
test()