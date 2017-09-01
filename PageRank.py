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
        userids = self.features.keys()
        # 将userids写入文件

        users_matrix = []
        iter = 0
        # 连接neo4j
        driver,session = neo4j.Conn()
        for id in userids:
            followings = neo4j.GetFollowings(driver,session,id)
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
            users_matrix.append(userRow)


        users_matrix = csr_matrix(users_matrix).T

        # 存储关系矩阵
        save_file = open("uMatrix.pickle","wb")
        pickle.dump(users_matrix,save_file)
        save_file.close()

        driver.close()
        session.close()
        return users_matrix

    def PageRank(self,uMatrix,fMatrix,d,PRMatrix,threshold,iterationN):
        NewPRMatrix = OldPRMatrix = PRMatrix
        iteration = 0
        rowN = NewPRMatrix.shape[0]
        while True:
            # NewPRMatrix = fMatrix + d * uMatrix * OldPRMatrix
            NewPRMatrix = uMatrix * OldPRMatrix * d + fMatrix
            # for i in range(len(uMatrix)):
            #     # 取uMatrix第i列
            #     newPRMatrix.append(double(uMatrix[i] * OldPRMatrix * d + fMatrix[i,0]))
            #     count += 1
            #     print count
            # print newPRMatrix
            # NewPRMatrix = mat(newPRMatrix).T
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

    # 构造字典,读取PageRank结果,提取出影响力最大的前100位
    def GetTop100Users(self,path):
        open_file = open("PageRank_results.pickle")
        PRMatrix = pickle.load(open_file)
        open_file.close()
        uPR = {}
        user_ids = self.features.keys()
        for i,id in zip(range(len(user_ids)),user_ids):
            uPR[id] = PRMatrix[i]
        # 对uPR排序
        uPR = sorted(uPR.items(),key = lambda dic:dic[1],reverse=True)
        # 将前100的用户写入文件
        with open("InfluenceTop100","wb") as f:
            for user in uPR[:100]:
                f.write(user[0])
                f.write(" ")
                f.write(user[1])
                f.write("\n")

def test():
    method = PageRank(40,datapre.Features())
    # 获得出入度矩阵
    uMatrix = method.GetUserMatrix()

    # open_file = open("/home/duncan/uMatrix.pickle")
    # uMatrix = pickle.load(open_file)
    # open_file.close()
    # uMatrix = uMatrix.T

    # 转移矩阵
    fMatrix = mat([(1 - 0.85) / len(method.features) for i in range(len(method.features))]).T
    # 初始矩阵
    initPRMatrix = mat([1 for i in range(len(method.features))]).T

    result = method.PageRank(uMatrix,fMatrix,0.85,initPRMatrix,0.01,120)

    save_file = open("PageRank_results.pickle","wb")
    pickle.dump(result,save_file)
    save_file.close()

    method.GetTop100Users("PageRank_results.pickle")

test()
