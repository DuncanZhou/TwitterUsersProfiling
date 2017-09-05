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
        # 对test_set遍历,对每个其中的元素,用与profiles中的对其代表性最大的元素来标记其领域
        results = {}
        for element in test_set.keys():
            followings = set(neo4j.GetFollowings(driver,session,element))
            results[element] = self.features[max({profile:1.5 * metric.CRepre(self.features[profile],self.features[element]) if profile in followings else metric.CRepre(self.features[profile],self.features[element]) for profile in profiles}.items(),key=lambda dic:dic[1])[0]][5]

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
    # init.InitialMatrix(train_set)
    print "开始抽取代表性用户"
    for epsilon in epsilons:
        profiles1 = greedy.Greedy(100,train_set,datapre.CategoriesDistribution(),epsilon).SearchWithReplace()
        print "GB方法计算完成"
        profiles2 = kmediods.KMedoids(100,train_set,datapre.CategoriesDistribution(),epsilon).Search()
        print "kmedoids方法计算完成"
        profiles3 = sa.SAalgo(100,train_set,datapre.CategoriesDistribution(),epsilon,0.3,10,0.9).Search()
        print "sa方法计算完成"
        with open("%.3f" % epsilon,"wb") as f:
            f.write("方法:GB; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles1,test_set)))
            f.write("方法:kmedoids; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles2,test_set)))
            f.write("方法:SA; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles3,test_set)))
        print "方法:GB; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles1,test_set))
        print "方法:kmedoids; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles2,test_set))
        print "方法:SA; 典型阈值:%f; 代表性子集数量:100; 准确率:%.3f \n" % (epsilon,method.Classify(profiles3,test_set))

test()