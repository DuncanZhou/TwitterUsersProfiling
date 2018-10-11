#!/usr/bin/python
#-*-coding:utf-8-*-
'''@Date:18-10-10'''
'''@Time:下午1:24'''



import numpy as np
# from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import euclidean_distances

# AP聚类算法
# 此算法虽然不再需要设置聚类簇的个数,但仍需要设置Similarity(k,k),该值越大该点越有可能成为中心点

def euclideanDistance(X, Y):
    """计算每个点与其他所有点之间的欧几里德距离"""
    X = np.array(X)
    Y = np.array(Y)
    # print X
    return np.sqrt(np.sum((X - Y) ** 2))

def computeSimilarity(datalist):

    num = len(datalist)

    Similarity = []
    for pointX in datalist:
        dists = []
        for pointY in datalist:
            dist = euclideanDistance(pointX, pointY)
            if dist == 0:
                dist = 1.5
            dists.append(dist * -1)
        Similarity.append(dists)
        return Similarity


class AP:
    def __init__(self,users):
        self.users = users

    def apclustering(self):
        '''

        :param users: csv格式，转换成列表格式
        :return: 聚类簇中心以及各个聚类簇，用用户id表示
        '''

        features = [col for col in self.users.columns if col != "category" and col != 'userid']
        X = self.users[features].values.tolist()
        users = self.users.values.tolist()
        af = AffinityPropagation().fit(X)
        print "聚类完成"
        # 聚类中心的索引
        cluster_centers_indices = af.cluster_centers_indices_
        mediods = [users[cluster_centers_indices[i]][0] for i in xrange(len(cluster_centers_indices))]

        # 聚类个数
        n_clusters_ = len(cluster_centers_indices)
        print "聚类簇个数为%d" % n_clusters_
        # 得到每个点所对应的聚类簇
        labels = af.labels_

        clusters = {}
        # 输出每个中心对应的点
        for i in xrange(n_clusters_):
            elements = [users[k][0] for k in xrange(len(labels)) if labels[k] == i]
            clusters[mediods[i]] = elements
        return clusters

def test():
    category = "Entertainment"
    users = pd.read_csv("users/"+category+"Users.csv")
    print "共有用户%d" % len(users)
    ap = AP(users)
    clusters = ap.apclustering()

test()