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

    # 确定聚类簇的个数
    def GenerateK(self,total_number):
        '''

        :param total_number: 样本的总数
        :return: 返回k的大小
        '''
        if total_number >= 1 and total_number < 10000:
            k = 9
        elif total_number >= 10000 and total_number < 100000:
            k = int(self.alpha * total_number)
        else:
            k = 100
        return k

    # 根据字典的value值查找key值
    def find_key(self,dict,value):
        for key in dict.keys():
            if value == dict[key]:
                return key
        return None

    # k-means聚类
    def Cluster(self):
        k = self.GenerateK(len(self.features.keys()))
        k_seeds = set()
        k_means_vector = {}

        # 随即选择k个作为初始均值向量
        i = 0
        while len(k_seeds) < k:
            for key in self.features.keys():
                if self.features[key][5] == (i % 9) and key not in k_seeds:
                    k_seeds.add(key)
                    k_means_vector[len(k_seeds) - 1] = self.features[key]
                    break
            i += 1
        print "%d个种子已选好" % k
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
            print "聚类簇:%d,类别特征:%s,包含样本个数:%d" % (i,self.find_key(datapre.category_dic,k_means_vector[i][5]),len(cluster[i]))
        return cluster,k_means_vector















