#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import AffinityPropagation

# AP聚类算法
# 此算法虽然不再需要设置聚类簇的个数,但仍需要设置Similarity(k,k),该值越大该点约有可能成为中心点
def cluster(Similarity,damp):
    '''

    :param Similarity: 相似性矩阵 (对称矩阵),相似度矩阵是负值矩阵
    :param damp: 振荡系数
    :return:
    '''
    # 初始化Responsibility和Availability矩阵
    N = Similarity.shape[0]
    Responsibility = np.zeros([N,N])
    Availability = np.zeros([N,N])

    # 迭代更新矩阵
    MAX_ITERATIONS = 10
    iteration = 0
    total = set([i for i in xrange(N)])
    centers = set()
    while iteration < MAX_ITERATIONS:
        # 更新响应度矩阵
        # 记录旧的响应度矩阵
        Old_Responsibility = Responsibility
        AS = Availability + Responsibility
        # 生成每个元素该减的元素矩阵

        TempRow = np.matrix([[float(np.max(AS[row,list(total- set([i]))])) for i in xrange(N)] for row in xrange(N)])

        # 相减得到最新的矩阵
        New_Responsibility = Similarity - TempRow
        # 和振荡系数相操作
        Responsibility = damp * Old_Responsibility + (1- damp) * New_Responsibility

        # 更新可用性的矩阵
        # 记录可用性矩阵
        Old_Availability = Availability

        TempRow = np.matrix([[float(Responsibility[k,k] + np.sum(np.maximum(Responsibility[list(total-set([i,k])),k],0),axis=0)) for k in xrange(N)] for i in xrange(N)])
        Availability = np.minimum(TempRow,0)

        # 更新自用性
        TempRow = [np.sum(np.maximum(Responsibility[list(total- set([k])),k],0)) for k in xrange(N)]
        for k in xrange(N):
            Availability[k,k] = TempRow[k]
        # 和振荡系数相操作
        Availability = damp * Old_Availability + (1 -damp) * Availability

        iteration += 1
        print iteration
        # 统计中心点
        Res = Responsibility + Availability
        flag = False
        for i in xrange(N):
            if Res[i,i] > 0 and i not in centers:
                centers.add(i)
                flag = True
        if flag == False:
            break

    return centers

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

def test():
    # -1,-0.8,-0.1,-0.2;-0.7,-1,-0.1,-0.3;-0.3,-0.1,-1,-0.7;-0.1,-0.2,-0.9,-1
    # Similarity = np.matrix([[-1,-0.8,-0.1,-0.2],[-0.7,-1,-0.1,-0.3],[-0.3,-0.1,-1,-0.7],[-0.1,-0.2,-0.9,-1]])

    centers = [[1, 1], [-1, -1], [1, -1]]
    X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5,
                            random_state=0)

    # preference是设置自我的代表度
    af = AffinityPropagation(preference=-50).fit(X)

    # 得到聚类结果
    # 聚类中心的索引
    cluster_centers_indices = af.cluster_centers_indices_
    # 聚类个数
    n_clusters_ = len(cluster_centers_indices)
    # 得到每个点所对应的聚类中心
    labels = af.labels_

    # Plot result
    # import matplotlib.pyplot as plt
    # from itertools import cycle
    #
    # plt.close('all')
    # plt.figure(1)
    # plt.clf()
    #
    # colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    # for k, col in zip(range(n_clusters_), colors):
    #     class_members = labels == k
    #     cluster_center = X[cluster_centers_indices[k]]
    #     plt.plot(X[class_members, 0], X[class_members, 1], col + '.')
    #     plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
    #              markeredgecolor='k', markersize=14)
    #     for x in X[class_members]:
    #         plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
    #
    # plt.show()

    # 输出每个中心对应的点
    for i in xrange(n_clusters_):
        class_members = labels == i
        cluster_center = X[cluster_centers_indices[i]]
        print "聚类中心为(%d %d)" % (cluster_center[0],cluster_center[1])
        # 打印该聚类簇中的点
        print "该聚类簇中包含:"
        for x in X[class_members]:
            print "(%d,%d)" % (x[0],x[1])

    # Similarity = np.matrix(computeSimilarity(X))
    # res = cluster(Similarity,0.5)
    # print res

test()

