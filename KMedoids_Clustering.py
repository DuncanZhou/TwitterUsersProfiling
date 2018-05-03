#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# k-mediods,是k-means的一种变体.相较于k-means他不再是简单地选取一个均值作为聚类簇的质点,而是
# 寻找在聚类簇中距离之差之和最小的作为最新质点.同时,因为这样,该算法的复杂度高于k-means

import Initial as init
import numpy as np
import random

class KMedoidsCluster:
    def __init__(self,k,users,R):
        # 需要聚类的数据集合
        self.users = users
        # 定义最大迭代次数
        self.Max_iteration = 30
        # 定义聚类簇个数
        self.k_min = k
        # 代表性矩阵
        self.R = R


    # 计算质点到其聚类簇中其它点的代表性之和
    def CalcRepre(self,clusters,point):
        '''

        :param cluster: cluster为聚类簇,为list类型
        :param point: 质点
        :return:
        '''
        return sum(self.R[point][clusters])

    # 选取新的质点,代表性最大的作为新的质点
    def SelectNewMediod(self,clusters):
        results = {element:self.CalcRepre(clusters,element) for element in clusters}
        return (max(results.items(),key=lambda key:key[1]))[0]

    # 聚类
    def Cluster(self):
        k = self.k_min
        # 初始化种子
        k_seeds = set(random.sample(range(len(self.users)),k))
        # 聚类领域
        # 聚类簇
        cluster = {}

        # 开始迭代
        iteration = 0
        while iteration < self.Max_iteration:
            for seed in k_seeds:
                cluster[seed] = set()
                # 把种子加入
                cluster[seed] = cluster[seed] | {seed}

            # 对所有元素进行聚类
            for i in xrange(len(self.users)):
                # results = {seed:self.R[self.R_dic[seed],self.R_dic[key]] for seed in k_seeds}
                # results = {}
                # for seed in k_seeds:
                #     results[seed] = metric.Repre(self.features[seed],self.features[key])
                # 距离k_seeds中的id最近,并入id聚类簇中
                if i in k_seeds:
                    continue
                id = np.argmax(self.R[list(k_seeds),i])
                id = list(k_seeds)[id]
                # 并入该聚类簇中
                cluster[id] = cluster[id] | set([i])
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


    # 聚类结束
    def Search(self):
        pass



def test():
    k_clusters = [10,15,20]
    users,R,id_list,g = init.Init("Actor")
    clustering = KMedoidsCluster(k_clusters[0],users,R)
    clustering.Cluster()
test()