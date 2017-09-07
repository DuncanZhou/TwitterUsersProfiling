#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import DataPrepare as datapre
import Metric as metric
import numpy as np
import pickle
import TwitterWithNeo4j as neo4j

# 初始化代表性矩阵
def InitialMatrix(features):
    print "开始初始化"
    people = datapre.People(features)
    categories = datapre.GetUserCategory()
    print "连接neo4j数据库"
    driver,session = neo4j.Conn()
    print "连接成功"
    for category in categories:
        tuples = people[category]
        # 两重循环计算代表性矩阵
        R = []
        print len(tuples)
        count = 0
        for id in tuples:
            followers = set(neo4j.GetFollowers(driver,session,id))
            row = []
            for id1 in tuples:
                if id1 in followers:
                    row.append(1.5 * metric.Repre(features[id],features[id1]))
                else:
                    row.append(metric.Repre(features[id],features[id1]))
            R.append(row)
            count += 1
            print count
        # 持久化代表性矩阵
        R = np.asarray(R)
        np.save("new%sRepresentativeMatrix.npy" % category,R)
        # 将用户id在矩阵中对应的行保存
        R_dic = {}
        for id,i in zip(tuples,xrange(len(tuples))):
            R_dic[id] = i
        save_file = open("new%sRepresentativeDictionary.pickle" % category,"wb")
        pickle.dump(R_dic,save_file)
        save_file.close()
        print category
    driver.close()
    session.close()



# InitialMatrix(datapre.Features())