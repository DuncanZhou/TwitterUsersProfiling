#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


# split each attribute and argmax the sumarization of the representativeness of all attributes

import math
import Distance as dist
import Metric as metric
import DataPrepare as datapre
import time
import numpy as np
import os
import pickle
import Initial

# 每个样本的格式[Followers,Activity,Influence,following,location,category,Interests_tags,userid]

# 对该算法做以下改进,在贪心过程中保证使得领域的分布和原来分布相同


# sigmoid函数,挤压函数
def sigmoid(x):
    return 1 * 1.0 / (1 + math.exp(-x))

# define the representativeness between users
def Repre(alpha,u,v):
    # include relationship, influence, activity, interest_tags
    if u == v:
        return 1
    if u[5] != v[5]:
        return 0
    distance = dist.distance(u, v)
    return (2 * sigmoid(1.0 / distance) - 1) * alpha


# search profiles
def Search(features,categories,epsilon,k,beta):
    Repre = {}
    for category in categories.keys():
        Repre[category] = np.load("new%sRepresentativeMatrix.npy" % category)
    Repre_id = {}
    for category in categories:
        open_file = open("new%sRepresentativeDictionary.pickle" % category)
        Repre_id[category] = pickle.load(open_file)
        open_file.close()

    # 每次并入使得目标函数最小化
    profiles = set()
    people = datapre.People(features)
    print "数据集装载完毕"
    for category in categories.keys():
        # p_number为该领域需要的人数
        p_number = (int)(k * categories[category]) + 1
        # tuples为该领域所有的人
        tuples = people[category]

        if not os.path.exists("new%sRepresentativeMatrix.npy" % category):
            pass
        else:
            # 加载矩阵
            # open_file = open("new%sRepresentativeMatrix.pickle" % category)
            # R = pickle.load(open_file)
            # open_file.close()
            # 换一种加载方式
            # R = np.load("new%sRepresentativeMatrix.npy" % category)
            R = Repre[category]
        rowN = len(tuples)
        results_vector = np.asarray([0 for i in xrange(rowN)])
        # 得到了代表性矩阵后
        count = 0
        has = {}
        while count < p_number:
            # results = {i:sum(max(x,y) for x,y in zip(R[i],results_vector)) for i in xrange(rowN) if i not in has}
            results = {i:sum(np.max(np.vstack((R[i],results_vector)),axis=0)) for i in xrange(rowN) if i not in has}
            results = sorted(results.items(),key=lambda key:key[1],reverse=True)
            for result in results:
                if metric.checkOneTypical(features,tuples[result[0]],profiles,epsilon):
                    to_add = result[0]
                    has[to_add] = tuples[to_add]
                    profiles.add(tuples[to_add])
                    # 更新
                    results_vector = np.max(np.vstack((R[to_add],results_vector)),axis=0)
                    # results_vector = [max(x,y) for x,y in zip(R[to_add],results_vector)]
                    count += 1
                    print "the number of profiles is %d" % len(profiles)
                    break
    # return list(profiles)
    print metric.AttributeRepresentative(features,profiles)
    print "开始删除多余结点"
    # 先统计每个领域的人数,用以统计该领域是否能被减少人数
    categories = datapre.DomainDistribution(profiles,features)
    # 遍历,如果将其排除,那么损耗将会减少多少,将排除后损失依然小的排除
    to_delete = len(profiles) - k
    has_category = set()
    count = 0
    results = {}
    for category in categories.keys():
        if categories[category] == 1 or categories[category] == int(categories[category] * k):
            # 该领域不能删除
            continue
        profile_domain = set([id for id in profiles if features[id][5] == category])
        if os.path.exists("new%sRepresentativeMatrix.npy" % category):
            # 加载矩阵
            # open_file = open("%sRepresentativeMatrix.pickle" % category)
            # R = pickle.load(open_file)
            # open_file.close()
            # R = np.load("new%sRepresentativeMatrix.npy" % category)
            R = Repre[category]
            # 加载id字典
            # open_file = open("new%sRepresentativeDictionary.pickle" % category)
            # R_dic = pickle.load(open_file)
            # open_file.close()
            R_dic = Repre_id[category]
            # 该领域的代表性人物对应的所有行
            rows = set([R_dic[id] for id in profile_domain])
            original = sum(np.max(np.asarray([R[i] for i in rows]),axis=0))
            subresults = {profile:(original - sum(np.max(np.asarray([R[i] for i in (rows - {R_dic[profile]})]),axis=0))) for profile in profile_domain}

            to_delete_id = (min(subresults.items(),key=lambda key:key[1]))[0]
            results[to_delete_id] = subresults[to_delete_id]
    # print len(results)
    results = sorted(results.items(),key=lambda key:key[1])
    for result in results:
        profiles.remove(result[0])
        print "the number of profiles is %d" % len(profiles)
        has_category.add(features[result[0]][5])
        count += 1
        if count == to_delete:
            break
    return profiles

def Run():
    alphas = ["1.8","1.65","1.5","1.35","1.2"]
    numbers = [40,60,80,100,120]
    epsilons = [0.1558,0.1557,0.1556]
    features = datapre.Features()
    for alpha in alphas:
        Initial.InitialMatrix(features,float(alpha))
        if not os.path.exists("S3" + alpha):
            os.mkdir("S3" + alpha)
        for number,epsilon in zip(numbers,epsilons):
            start_time = time.time()
            profiles = Search(features,datapre.CategoriesDistribution() ,epsilon,number,1)
            end_time = time.time()
            with open("S3%s/%d_%.4f" % (alpha,number,epsilon),"wb") as f:
                f.write("cost %f s" % (end_time - start_time))
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features, profiles)))
                f.write("\n")
                for profile in profiles:
                    f.write(profile + "\t")
Run()
