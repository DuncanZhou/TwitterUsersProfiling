#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
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

        # 将剩余的用户加入
        left = set(self.features.keys()) - set(train_set.keys())
        for id in left:
            test_set[id] = self.features[id]
        return train_set,test_set

    # 用每个方法提取出来的代表性人物来做NN分类,并计算准确率
    def Classify(self,profiles,test_set):
        pass

def test():
    method = Classifier(datapre.Features())
    train_set,test_set = method.Split()
    print len(train_set),len(test_set)
test()