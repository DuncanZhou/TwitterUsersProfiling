#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import EM_Clustering as em
import DataPrepare as datapre
import Metric as metric
import heapq

# 定义一个小顶堆
class MinHeap:

    def __init__(self):
        self.data = []

    def Push(self, elem):
        if len(self.data) == 0:
            heapq.heappush(self.data,elem)

        topk_small = self.data[0]
        if elem[1] < topk_small[1]:
            heapq.heapreplace(self.data, elem)

# 递归聚类
class Recursion_Cluster:
    def __init__(self):
        # 全局特征向量集
        self.features = datapre.Features()
        # 定义代表性向量最小个数
        self.k_min = 9
        # 定义迭代次数
        self.Max_iteration = 100
        # 定义聚类方法
        self.cmethod = em.EMCluster()

    def Search(self):
        # 初始的聚类集合是全集,为默认设置
        cluster,k_seeds,seeds_loss = self.cmethod.Cluster()
        s_current = {}
        for seed in k_seeds:
            s_current[seed] = self.features[seed]
        Loss_current = metric.metric(self.features,s_current)
        # 开始继续迭代添加
        iteration = 0
        while iteration < self.Max_iteration:
            old_size = len(s_current)
            # minHeap = MinHeap()
            to_check = []
            # 对每个子的聚类簇继续聚类
            for clusters in cluster:
                # clusters是一个元素id的集合
                cluster_vec = {}
                for id in clusters:
                    cluster_vec[id] = self.features[id]
                # 使用聚类方法
                self.cmethod.features = cluster_vec
                subcluster,sub_k_seeds,seeds_loss = self.cmethod.Cluster()
                # 使用最小堆尽然使结果降低了
                # for seed in seeds_loss.keys():
                #     minHeap.Push((seed,seeds_loss[seed]))
                for seed in sub_k_seeds:
                    to_check.append(seed)
            # to_check = minHeap.data
            # 对加入的新的元素进行判断
            for check in to_check:
                # s_current[check[0]] = self.features[check[0]]
                s_current[check] = self.features[check]
                if metric.metric(self.features,s_current) >= Loss_current:
                    s_current.pop(check)
            iteration += 1
            print "迭代%d次" % iteration
            if len(s_current) == old_size:
                break
        return s_current


