#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
'''@Date: 18-7-4'''
'''@Time: 下午9:18'''

# step1: Clustering (characteristics)
# step2: neighbours in each cluster / neighbours > threshold 进行shift到另一个聚类簇中
# step3: Community Detection
# step4: Sampling

import KMedoids_Clustering as KMedoid
from networkx.algorithms.community import greedy_modularity_communities
import Metric
import numpy as np

class Method1:
    def __init__(self,users,R,g,alpha,lam,category,dataset):
        # 用户特征向量集
        self.users = users
        # 代表性矩阵
        self.R = R
        # 用户拓扑图
        self.g = g
        # 采样算法参数
        self.lam = lam
        # 采样率
        self.alpha = alpha
        # 领域
        self.category = category
        # 数据集
        self.dataset = dataset

    # step1: 根据特征聚类
    def ClusteringByCharacteristics(self,users,R,k):
        # params k : 聚类簇的个数
        ids = list(users.id)
        kmedoid = KMedoid.KMedoidsCluster(k,ids,users,R,None,0)
        # 聚类完成
        cluster,seeds,id_cluster = kmedoid.Cluster()
        # 返回结果是聚类字典
        return id_cluster

    # step2: 对聚类簇进行社区发现
    def CommunityDetectionOnCluster(self,clusters,g):
        # 得到聚类簇的子图
        sub_graph = g.subgraph(clusters)
        community = list(greedy_modularity_communities(sub_graph))
        # 对不在community的结点单独作为一个社区
        left_ids = set(clusters) - (map(lambda a,b:set(a) | set(b),community))
        for id in left_ids:
            community.append([id])
        # 返回社区发现结果
        return community

    # 步骤2至步骤3的过渡步骤，将结果整理成小组形式
    def GenerateResults(self,id_cluster,g):
        results = {}
        # 存储每个聚类簇的大小
        clusters_num = {i:len(id_cluster[i]) for i in id_cluster.keys()}
        for key in id_cluster.keys():
            clusters = id_cluster[key]
            results[key] = self.CommunityDetectionOnCluster(clusters,g)
        return results,clusters_num

    # step3: Sampling(shift步骤先省略)
    def Sampling(self,clusters_withC,clusters_num):
        '''

        :param clusters_withC: 特征和拓扑分好类
        :param clusters_num: 特征聚类簇的大小
        :return:
        '''
        # clusters为每个聚类簇中已分好的小组，然后从这每个聚类簇中每个小组中采样
        # 贪心算法(使得目标函数增加最大的点加入)
        theta = {}
        profiles = set()
        # 给theta初始化
        for key in clusters_withC.keys():
            for i in range(len(clusters_withC[key])):
                theta[(key,i)] = 0

        # 从每个聚类簇中加入
        metric = Metric.Metrics(None,None,self.R)
        total = len(self.users)
        k = self.alpha * total
        while len(profiles) < k:

            results = {}
            # 对每个聚类簇遍历
            for key in clusters_withC.keys():
                cluster_weight = clusters_num[key] * 1.0 / total
                # 对每个社区遍历
                for i in range(len(clusters_withC[key])):
                    community = clusters_withC[key][i]
                    community_weight = len(community) * 1.0 / clusters_num[key]
                    # 对每个点加入计算目标函数增量
                    for j in range(len(community)):
                        profiles.add(community[j])
                        rc = metric.Rc(community,profiles)
                        rt = metric.Rt(community,profiles)
                        results[community[j]] = cluster_weight * community_weight * (self.lam * rc + (1 - self.lam * rt)) - theta[(key,i)]
                        profiles.remove(community[j])

            # 从results中选取增量最大的加入
            to_add = max(results,key=results.get)
            profiles.add(to_add)

        # 输出p, r, f1
        metric.PR(profiles,self.alpha,self.category,self.alpha,self.dataset)

        return profiles