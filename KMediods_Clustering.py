#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# k-mediods,是k-means的一种变体.相较于k-means他不再是简单地选取一个均值作为聚类簇的质点,而是
# 寻找在聚类簇中距离之差之和最小的作为最新质点.同时,因为这样,该算法的复杂度高于k-means

import DataPrepare as datapre
import Distance as dist
import math

class KMediodsCluster:
    def __init__(self):
        # 全局变量,特征向量集
        self.features = datapre.Features()
        # 定义迭代次数
        self.Max_iteration = 100
        # 定义聚类簇个数
        self.k_min = 9

    # 计算质点到其聚类簇中其它点的距离之和
    def CalcDistance(self,clusters,point):
        '''

        :param cluster: cluster为聚类簇,为list类型
        :param point: 质点
        :return: 距离绝对值之和
        '''
        sum = 0
        for seed in clusters:
            sum += dist.distance(self.features[seed],self.features[point])
        return sum

    # 选取新的质点
    def SelectNewMediod(self,clusters):
        min = self.CalcDistance(clusters,clusters[0])
        min_id = 0
        for i in clusters:
            if self.CalcDistance(clusters,i) < min:
                min = self.CalcDistance(clusters,i)
                min_id = i
        return min_id

    # 聚类
    def Cluster(self):
        k = self.k_min
        # 初始化种子
        k_seeds = list(datapre.Initial(self.features,k))
        # 聚类簇
        cluster = []

        # 开始迭代
        iteration = 0
        while iteration < self.Max_iteration:
            for i in range(k):
                cluster.append(set())

            # 对所有元素进行聚类
            for key in self.features.keys():
                # 计算样本与各均值向量距离,距离最近的向量划入相应的簇
                min = dist.distance(self.features[key],self.features[k_seeds[0]])
                i = 1
                id = 0
                while i < k:
                    if dist.distance(self.features[key],self.features[k_seeds[i]]) < min:
                        min = dist.distance(self.features[key],self.features[k_seeds[i]])
                        id = i
                    i += 1
                # 并入该聚类簇中
                new_element = set()
                new_element.add(key)
                cluster[id] = cluster[id] | new_element

            # 更新质点向量
            # flag来判断是否需要停止迭代
            flag = True
            # 对每个聚类簇分别判断
            i = 0
            while i < k:
                new_mediod = self.SelectNewMediod(list(cluster[i]))
                if new_mediod != k_seeds[i]:
                    k_seeds[i] = new_mediod
                    flag == False
                i += 1

            if flag == True:
                # 停止迭代
                break
            iteration += 1
            print "迭代%d次" % iteration

        s_current = {}
        for seed in k_seeds:
            s_current[seed] = self.features[seed]

        return cluster,s_current

