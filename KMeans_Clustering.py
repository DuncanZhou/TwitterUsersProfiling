#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# K-Means算法的变体,对于连续型属性采用均值,对于离散型属性取聚类簇中频率高的离散属性值
import DataPrepare as datapre
import Distance as dist
import collections

class KMeansCluster:

    def __init__(self):

        # 全局变量,特征向量集
        self.features = datapre.Features()
        # 定义alpha
        self.alpha = 0.001
        # 定义迭代次数
        self.Max_iteration = 100
        # 定义聚类簇个数
        self.k_min = 9

    # 确定聚类簇的个数

    # k-means聚类
    def Cluster(self):
        k = self.k_min
        k_seeds = datapre.Initial(self.features,self.k_min)
        k_means_vector = {}

        # 随机选择k个作为初始均值向量(使得选择的种子包含了所有的类别
        for seed in k_seeds:
            k_means_vector[seed] = self.features[seed]

        # 开始聚类
        iteration = 0
        while iteration < self.Max_iteration:
            # 聚类簇
            cluster = []
            for i in range(k):
                cluster.append(set())

            for key in self.features.keys():
                # 计算样本与各均值向量距离,距离最近的向量划入相应的簇
                min = dist.distance(self.features[key],k_means_vector[0])
                i = 1
                id = 0
                while i < k :
                    if dist.distance(self.features[key],k_means_vector[i]) < min:
                        min = dist.distance(self.features[key],k_means_vector[i])
                        id = i
                    i += 1
                # 并入该聚类簇中
                new_element = set()
                new_element.add(key)
                cluster[id] = cluster[id] | new_element

            # 重新更新均值向量,即k_means_vector
            i = 0
            flag = True
            while i < k:
                # 先计算连续值的平均值
                sum_fratio = 0
                sum_activity = 0
                sum_influence = 0
                categories = []
                interest_tags = []
                location = []
                for id in cluster[i]:
                    sum_fratio += self.features[id][0]
                    sum_activity += self.features[id][1]
                    sum_influence += self.features[id][2]
                    for interest in self.features[id][3]:
                        interest_tags.append(interest.lower())
                    location.append(self.features[id][4])
                    categories.append(self.features[id][5])
                number = len(cluster[i])
                interets_tags = dict(collections.Counter(interest_tags))
                new_interst = map(lambda x:x[0],sorted(interets_tags.items(),key = lambda interest_tags:interest_tags[1],reverse=True)[:10])
                category = sorted(dict(collections.Counter(categories)).items(),key = lambda x:x[1],reverse=True)[0][0]
                location = sorted(dict(collections.Counter(location)).items(),key = lambda x:x[1],reverse=True)[0][0]
                new_means_vector = (sum_fratio / number,sum_activity / number,sum_influence / number,new_interst,location,category)
                # 更新均值向量
                if new_means_vector[0] == k_means_vector[i][0] and new_means_vector[1] == k_means_vector[i][1] and new_means_vector[2] == k_means_vector[i][2] and new_means_vector[4] == k_means_vector[i][4] and new_means_vector[5] == k_means_vector[i][5]:
                    i += 1
                    continue
                k_means_vector[i] = new_means_vector
                flag = False
                i += 1

            if flag == True:
                # 均值向量全未改变,终止迭代
                break
            iteration += 1
            print "迭代%d次" % iteration

        # 对聚类结果进行输出
        for i in range(len(cluster)):
            print "聚类簇:%d,类别特征:%s,包含样本个数:%d" % (i,datapre.find_key(datapre.category_dic,k_means_vector[i][5]),len(cluster[i]))
        return cluster,k_means_vector















