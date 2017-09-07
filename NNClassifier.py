#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import Metric as metric
import GreedyAlgorithm as greedy
import SAalgo as sa
import KMedoids_Clustering as kmediods
import Initial as init
import TwitterWithNeo4j as neo4j
import PageRank as pr
import pickle
from numpy import *

class Classifier:
    def __init__(self,features):
        self.features = features

    # 先将数据集进行3:7划分,形成训练集和测试集
    def Split(self):
        # 返回结果为训练集和测试集
        train_set = {}
        test_set = {}
        # 对原集中每个领域取3/10加入train_set,取7/10加入test_set
        people = datapre.People(self.features)
        categories = datapre.GetUserCategory()
        for category in categories:
            domain_people = people[category]
            train_set_number = int(len(domain_people) * 0.3) + 1
            count = 0
            for id in domain_people:
                if count < train_set_number:
                    train_set[id] = self.features[id]
                    count += 1
                else:
                    break
        # 将剩余的用户加入
        left = set(self.features.keys()) - set(train_set.keys())
        for id in left:
            test_set[id] = self.features[id]
        return train_set,test_set

    # 用每个方法提取出来的代表性人物来做NN分类,并计算准确率
    def Classify(self,profiles,test_set):
        print "连接neo4j数据库"
        driver,session = neo4j.Conn()
        # 获取profiles的followers,并以字典存储
        followers = {}
        for profile in profiles:
            followers[profile] = set(neo4j.GetFollowers(driver,session,profile))

        # 对test_set遍历,对每个其中的元素,用与profiles中的对其代表性最大的元素来标记其领域
        results = {}
        for element in test_set.keys():
            # followings = set(neo4j.GetFollowings(driver,session,element))
            results[element] = self.features[max({profile:1.5 * metric.CRepre(self.features[profile],self.features[element]) if element in followers[profile] else metric.CRepre(self.features[profile],self.features[element]) for profile in profiles}.items(),key=lambda dic:dic[1])[0]][5]

        # 计算准确性
        count = 0
        for result in results.keys():
            if self.features[result][5] == results[result]:
                count += 1
        print "Accuracy is %.3f" % (count * 1.0 / len(results))
        driver.close()
        session.close()
        return (count * 1.0 / len(results))


def test():
    method = Classifier(datapre.Features())
    train_set,test_set = method.Split()
    print "数据集分割完成"
    print "训练集和测试集数量为:%d,%d" % (len(train_set),len(test_set))
    # 三个方法分别在train_set中寻找100个代表性人物,用代表性人物来分类test_set
    epsilons = [0.1560,0.1556,0.1555]
    # 将PageRank提取出来的100个用户也来做个分类
    # PageRank_method = pr.PageRank(40,train_set,datapre.GetUserCategory())
    # # 获得出入度矩阵
    # uMatrix = PageRank_method.GetUserMatrix()
    # #
    # # 转移矩阵
    # fMatrix = mat([(1 - 0.85) / len(train_set.keys()) for i in range(len(train_set.keys()))]).T
    # # 初始矩阵
    # initPRMatrix = mat([1 for i in range(len(train_set.keys()))]).T
    # # result为影响力分数结果
    # PRMatrix = PageRank_method.PageRank(uMatrix,fMatrix,0.85,initPRMatrix,0.01,120)
    # user_ids = train_set.keys()
    # uPR = {}
    # for i,id in zip(range(len(user_ids)),user_ids):
    #     uPR[id] = PRMatrix[i]
    # # 对uPR排序
    # uPR = sorted(uPR.items(),key = lambda dic:dic[1],reverse=True)
    # profiles = [u[0] for u in uPR[:100]]
    # print "PageRank的分类准确性为%.3f" % method.Classify(profiles,test_set)
    # return
    # epsilons = [0.1556,0.1555]
    # epsilons = [0.1560]
    # init.InitialMatrix(train_set)
    number = [40,60,80,100]
    print "开始抽取代表性用户"
    for epsilon in epsilons:
        with open("%.4f" % epsilon,"wb") as f:
            for k in number:
                profiles1 = greedy.Greedy(k,train_set,datapre.CategoriesDistribution(),epsilon).SearchWithReplace()
                print "GB方法计算完成"
                profiles2 = kmediods.KMedoids(k,train_set,datapre.CategoriesDistribution(),epsilon).Search()
                print "kmedoids方法计算完成"
                profiles3 = sa.SAalgo(k,train_set,datapre.CategoriesDistribution(),epsilon,0.3,10,0.9).Search()
                print "sa方法计算完成"

                accuracy1 = method.Classify(profiles1,test_set)
                f.write("方法:GB; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy1))
                accuracy2 = method.Classify(profiles2,test_set)
                f.write("方法:kmedoids; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy2))
                accuracy3 = method.Classify(profiles3,test_set)
                f.write("方法:SA; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy3))

                print "方法:GB; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy1)
                print "方法:kmedoids; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy2)
                print "方法:SA; 典型阈值:%f; 代表性子集数量:%d; 准确率:%.3f \n" % (epsilon,k,accuracy3)

test()