#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import numpy as np

# AP聚类算法
def cluster(Similarity,damp):
    '''

    :param Similarity: 相似性矩阵 (对称矩阵)
    :param damp: 振荡系数
    :return:
    '''
    # 初始化Responsibility和Availability矩阵
    N = Similarity.shape[0]
    Responsibility = np.zeros([N,N])
    Availability = np.zeroes([N,N])

    # 迭代更新矩阵
    MAX_ITERATIONS = 100
    iteration = 0
    total = set([i for i in N])
    while iteration < MAX_ITERATIONS:
        # 更新响应度矩阵
        # 记录旧的响应度矩阵
        Old_Responsibility = Responsibility
        AS = Availability + Responsibility
        # 生成每个元素该减的元素矩阵
        TempRow = np.matrix([[np.max(AS[row][list(total.remove(i))]) for i in xrange(N)] for row in xrange(N)])
        # 相减得到最新的矩阵
        New_Responsibility = Similarity - TempRow
        # 和振荡系数相操作
        Responsibility = damp * Old_Responsibility + (1- damp) * New_Responsibility

        # 更新可用性的矩阵
        # 记录可用性矩阵
        Old_Availability = Availability

        TempRow = np.matrix([[Responsibility[k,k] + np.maximum(Responsibility[list(total-set([i,k])),k]) for k in xrange(N)] for i in xrange(N)])
        Availability = np.minimum(TempRow,0)

        # 更新自用性
        TempRow = [np.sum(np.maximum(Responsibility[list(total.remove(k)),k])) for k in xrange(N)]
        for k in xrange(N):
            Availability[k,k] = TempRow[k]
        # 和振荡系数相操作
        Availability = damp * Old_Availability + (1 -damp) * Availability

        iteration += 1

