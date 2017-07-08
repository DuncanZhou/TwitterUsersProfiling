#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import KMeans_Clustering as kmean
import DataPrepare as datapre
import Distance as dist

# 随机选择k个作为初始聚类点
# 按代表性聚类,将剩余样本加入
# 每次聚类结束选择对当前聚类代表性最大的作为新的代表性聚类点
# 设置迭代次数和收敛条件

class EMCluster:
    def __init__(self):
        # 定义迭代次数
        self.Max_iteration = 100
        # 定义全局特征向量集
        self.features = datapre.Features()
        # 定义alpha,用来控制聚类簇个数
        self.alpha = 0.001
        # 定义代表性向量最小个数(因为人物领域的类别为9个)
        self.k_min = 9

    # 聚类函数
    def Cluster(self):
        '''

        :return: 聚类结果list(set())和每个聚类簇中最具代表性的元素list
        '''
        k = self.k_min
        k_seeds = list(datapre.Initial(self.features,self.k_min))

        # 开始聚类
        # 设置聚类次数
        iteration = 0
        while iteration < self.Max_iteration:
            # 聚类簇
            cluster = []
            for i in range(k):
                cluster.append(set())

            # 先按代表性划入相应的聚类簇中
            for key in self.features.keys():
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

            # 重新更新聚类簇中代表性向量,即k_representative_vector
            # 计算每个聚类簇中对其代表性最强(也就是距离之和最小)的元素重新加入k_representative_vector
            i = 0  # 对聚类簇计数
            flag = False
            while i < k:
                min = 0
                representative_id = k_seeds[i]
                # 计算该向量在当前聚类簇中的距离之和
                for id in cluster[i]:
                    min += dist.distance(self.features[id],self.features[representative_id])

                # 遍历该聚类簇中其他元素
                for id in cluster[i]:
                    distance = 0
                    for id2 in cluster[i]:
                        distance += dist.distance(self.features[id],self.features[id2])
                    if distance < min:
                        representative_id = id
                        min = distance

                # 替换新的代表性的向量
                if k_seeds[i] != representative_id:
                    k_seeds[i] = representative_id
                    # 需要继续迭代
                    flag = True

                i += 1

            if flag == False:
                # 收敛,停止迭代
                break
            iteration += 1
            print "迭代%d次" % iteration

        # 对聚类结果进行输出
        for i in range(len(cluster)):
            print "聚类簇:%d,类别特征:%s,包含样本个数:%d" % (i,kmean.KMeansCluster.find_key(datapre.category_dic,self.features[k_seeds[i]][5]),len(cluster[i]))
        return cluster,k_seeds










