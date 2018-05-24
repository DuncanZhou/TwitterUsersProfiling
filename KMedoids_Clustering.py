#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# k-mediods,是k-means的一种变体.相较于k-means他不再是简单地选取一个均值作为聚类簇的质点,而是
# 寻找在聚类簇中距离之差之和最小的作为最新质点.同时,因为这样,该算法的复杂度高于k-means

import Initial as init
import random
import numpy as np
from networkx.classes.function import all_neighbors
import Metric
import time
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.cluster import k_medoids_
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances

class KMedoidsCluster:
    def __init__(self,k,ids,users,R,g,need):
        # 需要聚类的数据集合
        self.ids = ids
        # 人物信息
        self.users = users
        # 定义最大迭代次数
        self.Max_iteration = 30
        # 定义聚类簇个数
        self.k_min = k
        # 代表性矩阵
        self.R = R
        # 拓扑结构
        self.g = g
        # 需要采样的人数
        self.need = need


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
        k_seeds = set(random.sample(self.ids,k))
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
            for i in self.ids:
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
            # 对每个聚类簇分别判断,同时需要更新cluster
            print "更新聚类中心"
            new_k_seeds = set()
            for seed in k_seeds:
                new_mediod = self.SelectNewMediod(list(cluster[seed]))
                new_k_seeds.add(new_mediod)
                if new_mediod != seed:
                    # 替换cluster[seed]的键值
                    cluster[new_mediod] = cluster[seed]
                    cluster.pop(seed)
                    # 需要继续迭代
                    flag = False
            k_seeds = new_k_seeds
            if flag == True:
                # 停止迭代
                break
            iteration += 1
            print "迭代%d次" % iteration
        print "聚类完成"
        id_cluster = {}
        for key in cluster.keys():
            ids = reduce(lambda x,y:x|y, [set([self.users.iloc[i]['userid']]) for i in cluster[key]])
            id_cluster[self.users.iloc[key]['userid']] = ids

        return cluster,k_seeds,id_cluster


    # 代表性子集对某个聚类簇的代表性
    def CalcRc(self,profiles,cluster):
        '''

        :param profiles: 代表性子集
        :param cluster: 某个聚类簇
        :return:
        '''
        maxes = np.max(self.R[list(profiles),:],axis=0)
        return np.sum(maxes[list(cluster)],axis=0) / len(cluster)

    # 代表性子集对某个聚类簇的拓扑代表性
    def CalcRt(self,profiles,cluster):
        '''

        :param profiles: 代表性子集
        :param cluster: 某个聚类簇
        :return:
        '''
        clusteri = reduce(lambda x,y:x | y,[set([self.users.iloc[i]['userid']]) for i in cluster])
        neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,str(self.users.iloc[u]['userid']))) if str(u) in self.g else set() for u in profiles])
        return len(neighbours & clusteri) * 1.0 / len(clusteri)

    # 采样
    def Sample(self,gamma,clusters,id_cluster):
        num = len(self.users)
        profiles = set()
        # 初始化每个cluster的Rc和Rt
        Rc = {i:0 for i in clusters.keys()}
        Rt = {i:0 for i in clusters.keys()}
        neighbours = {i:set() for i in id_cluster.keys()}
        while len(profiles) < self.need:
            results = {}
            # 对于不在profiles中的元素继续加入,加入使得F最大的元素
            # 从每个聚类簇中选取元素加入
            for key in clusters.keys():
                temp = {i:len(clusters[key]) * 1.0 / num * (gamma*self.CalcRc(profiles | set([i]),clusters[key]) - gamma*Rc[key]+(1-gamma)*(len(set(all_neighbors(self.g,self.users.iloc[i]['userid'])) & id_cluster[key]                                                                                                                                       - neighbours[key]) if self.users.iloc[i]['userid'] in self.g else 0)) for i in clusters[key] if i not in profiles}
                # 找到temp中增长最大的值和结果
                item = max(temp.items(),key=lambda key:key[1])
                results[item[0]] = item[1]
            # 从results找到增长最大的加入
            to_add = max(results.items(),key=lambda key:key[1])[0]
            # to_add = results.keys()[to_add]
            profiles.add(to_add)
            # 确定to_add属于哪个聚类簇
            for key in clusters.keys():
                if to_add in clusters[key]:
                    belong = key
                    break
            print len(profiles)
            # 更新belong的Rc和Rt,neigbours
            neighbours[belong] |= set(all_neighbors(self.g,self.users.iloc[to_add]['userid'])) if self.users.iloc[to_add]['userid'] in self.g else set()
            Rc[belong] = self.CalcRc(profiles,clusters[belong])
            Rt[belong] = self.CalcRt(profiles,clusters[belong])
        profiles = [self.users.iloc[i]['userid'] for i in profiles]
        return profiles

def test():
    # k_clusters = [10,15,20]
    # users,R,id_list,g = init.Init("Actor")
    # clustering = KMedoidsCluster(k_clusters[0],users,R,g,id_list,int(len(users) * 0.05))
    # start = time.time()
    features = ['friends','followers','statuses','favourites','gender','verified','city','urank']
    # cluster = clustering.ClusterWithoutMatrix(features)
    # cluster,seeds,id_cluster = clustering.Cluster()
    # 通过聚类筛选代表性人物

    # profiles = clustering.Sample(0.8,cluster,id_cluster)
    # end = time.time()
    # metric = Metric.Metrics(users,R,id_list,g)
    # rc,rt,rscore = metric.RScore(profiles)
    # print "cost %f s" % (end - start)
    # print "rc:%f,rt:%f,rscore:%f" % (rc,rt,rscore)

    # 实验sklearn的kmeans算法
    users = pd.read_csv("users/"+"Common"+"Users.csv")
    X = np.asarray(users[features])
    # kmeans = KMeans(n_clusters=10,random_state=0).fit(X)
    kmedoids = k_medoids_.KMedoids(n_clusters=10,random_state=0).fit(X)
    # 输出label
    # print kmeans.cluster_centers_
# test()