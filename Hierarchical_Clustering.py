#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre

class HierarchicalCluster:
    def __init__(self):
        # 定义alpha
        self.alpha = 0.001

        # 全局变量,特征向量集
        self.features = datapre.Features()

    # 设定聚类簇的个数k(一般情况下,k大小和已知的样本类别数相同)

    # 确定聚类簇的个数
    def GenerateK(self,total_number):
        '''

        :param total_number: 样本呢总数
        :return: 返回k的大小
        '''
        if total_number >= 1 and total_number < 1000:
            k = 5
        elif total_number >= 1000 and total_number < 100000:
            k = int(self.alpha * total_number)
        else:
            k = 100
        return k

    # 计算两个聚类簇之间的最小距离
    def CalcMin(self,cluster1,cluster2):
        min = dist.distance(self.features[cluster1[0]],self.features[cluster2[0]])
        for c1 in cluster1:
            for c2 in cluster2:
                if dist.distance(self.features[c1],self.features[c2]) < min:
                    min = dist.distance(self.features[c1],self.features[c2])
        return min

    # 计算两个聚类簇之间的最大距离
    def CalcMax(self,cluster1,cluster2):
        max = dist.distance(self.features[cluster1[0]],self.features[cluster2[0]])
        for c1 in cluster1:
            for c2 in cluster2:
                if dist.distance(self.features[c1],self.features[c2]) > max:
                    max = dist.distance(self.features[c1],self.features[c2])
        return max

    # 计算两个聚类簇之间的平均距离
    def CalcAvg(self,cluster1,cluster2):
        sum = 0
        for c1 in cluster1:
            for c2 in cluster2:
                sum += dist.distance(self.features[c1],self.features[c2])
        avg = sum * 1.0 / (len(cluster1) * len(cluster2))
        return avg

    # 返回距离最小的两个聚类簇
    def CalcMinDistance(self,cluster):
        # 找出距离最近的两个聚类簇

        min = self.CalcAvg(cluster[0],cluster[1])

        c1 = cluster[0]
        c2 = cluster[1]
        for i in range(len(cluster)):
            j = i + 1
            while j < len(cluster):
                if i != j and self.CalcAvg(cluster[i],cluster[j]) < min:
                    min = self.CalcAvg(cluster[i],cluster[j])
                    c1 = cluster[i]
                    c2 = cluster[j]
                j += 1
        return c1,c2

    # 聚类方法
    def Cluster(self):
        '''

        :param features: 特征向量全集
        :param k: 聚类簇的个数
        :return: 返回聚类结果集
        '''
        k = self.GenerateK(len(self.features.keys()))
        # 初始化过程,将每个样本都看做一个聚类簇
        cluster = []
        for key in self.features.keys():
            cluster_set = set()
            cluster_set.add(key)
            cluster.append(cluster_set)
        # 设置当前聚类簇个数current
        current = len(cluster)
        while current > k:
            # 找出距离最近的两个聚类簇
            c1,c2 = self.CalcMinDistance(cluster)
            # 对最小的合并
            cluster.remove(c1)
            cluster.remove(c2)
            c = c1 | c2
            cluster.append(c)
            current -= 1
            print "reduce to %d clusters" % current
        return cluster