#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


import numpy as np

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
    MAX_ITERATIONS = 100
    iteration = 0
    total = set([i for i in xrange(N)])
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

    # 统计中心点
    Res = Responsibility + Availability
    Res = np.argmax(Res,axis=1).tolist()
    return Res

def test():
    # -1,-0.8,-0.1,-0.2;-0.7,-1,-0.1,-0.3;-0.3,-0.1,-1,-0.7;-0.1,-0.2,-0.9,-1
    Similarity = np.matrix([[-1,-0.8,-0.1,-0.2],[-0.7,-1,-0.1,-0.3],[-0.3,-0.1,-1,-0.7],[-0.1,-0.2,-0.9,-1]])
    centers = cluster(Similarity,0.5)
    print centers

test()

