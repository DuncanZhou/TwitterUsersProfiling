#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
from numpy import *
import TwitterWithNeo4j as neo4j
from scipy.sparse import csr_matrix
import DataPrepare as datapre
import pickle

class PageRank:
    def __init__(self,k,features):
        self.k = k
        self.features = features

    def GetUserMatrix(self):
        userids = set(self.features.keys())
        users_matrix = []
        iter = 0
        for id in userids:
            followings = neo4j.GetFollowers(id)
            userRow = []
            if len(followings) != 0:
                for id1 in userids:
                    if id1 in followings:
                        userRow.append(1)
                    else:
                        userRow.append(0)
                userRow = map(lambda element:element * 1.0 / len(followings),userRow)
            else:
                userRow = [0 for i in range(len(userids))]
            iter += 1
            print iter
            user_matrix = csr_matrix(userRow)
            users_matrix.append(user_matrix)


        return users_matrix

    def PageRank(self,uMatrix,fMatrix,d,PRMatrix,threshold,iterationN):
        NewPRMatrix = OldPRMatrix = PRMatrix
        iteration = 0
        rowN = NewPRMatrix.shape[0]
        while True:
            # 将下面的公式转换一下
            newPRMatrix = []
            # NewPRMatrix = fMatrix + d * uMatrix * OldPRMatrix
            for i in range(len(uMatrix)):
                # 取uMatrix第i列
                column = [matrix[0,i] for matrix in uMatrix]

                newPRMatrix.append(double(column * OldPRMatrix * d + fMatrix[i,0]))
            # print newPRMatrix
            NewPRMatrix = mat(newPRMatrix).T
            flag = True
            iteration += 1
            if iteration == iterationN:
                break
            for i in range(rowN):
                if math.fabs(NewPRMatrix[i,0] - OldPRMatrix[i,0]) > threshold:
                    flag = False
                    break
            if flag == True:
                break
            OldPRMatrix = NewPRMatrix
            print "迭代%d次" % iteration
        print "迭代次数%d" % iteration
        return NewPRMatrix


def test():
    method = PageRank(40,datapre.Features())
    # 获得出入度矩阵
    uMatrix = method.GetUserMatrix()
    # 转移矩阵
    fMatrix = mat([(1 - 0.85) / len(method.features) for i in range(len(method.features))]).T
    # 初始矩阵
    initPRMatrix = mat([1 for i in range(len(method.features))]).T

    result = method.PageRank(uMatrix,fMatrix,0.85,initPRMatrix,0.01,120)

    save_file = open("PageRank_results.pickle","wb")
    pickle.dump(result,save_file)
    save_file.close()

test()
