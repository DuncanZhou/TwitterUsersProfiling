#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import math
import random

a = 2
b = 50
Sampling_Number = 1000

# sigmoid函数,挤压函数
def sigmoid(x):
    return 1 * 1.0 / (1 + math.exp(-x))

#  属性特征损耗
def AttributeLoss(origin_features,profile_features):
    loss = 0
    for key in origin_features.keys():
        list = [dist.distance(origin_features[key],profile_features[u]) for u in profile_features.keys()]
        loss += min(list)
    return loss

# 领域分布损耗
def DistributionLoss(original_features,profile_features):
    categories = {}
    for key in original_features.keys():
        if original_features[key][5] not in categories.keys():
            categories[original_features[key][5]] = 1
        else:
            categories[original_features[key][5]] += 1
    for key in categories.keys():
        categories[key] = categories[key] * 1.0 / len(original_features)

    profile_categories = {}
    for key in profile_features.keys():
        if profile_features[key][5] not in profile_categories.keys():
            profile_categories[profile_features[key][5]] = 1
        else:
            profile_categories[original_features[key][5]] += 1

    for key in profile_categories.keys():
        profile_categories[key] = profile_categories[key] * 1.0 / len(profile_features)

    # 统计损耗
    loss = 0
    for key in categories.keys():
        if key not in profile_categories.keys():
            loss += 1
        else:
            loss += pow(categories[key] - profile_categories[key],2)
    return math.sqrt(loss)

# 子集内部差异性
def Dissimilarity(profile_features):
    # 先将所有人分类
    categories = {}
    for key in profile_features.keys():
        if profile_features[key][5] not in categories.keys():
            list = [key]
            categories[profile_features[key][5]] = list
        else:
            categories[profile_features[key][5]].append(key)

    # 寻找每个领域与其他领域之间的相似度
    total_similarity = 0
    for key1 in categories.keys():
        targets = categories[key1]
        similarity = 0
        for key2 in categories.keys():
            if key2 != key1:
                other = categories[key2]
                # 在target和other中寻找距离最小的值
                minimals = []
                for id1 in targets:
                    minimals.append(min([dist.distance(profile_features[id1],profile_features[id2]) for id2 in other]))
                similarity += 2 * sigmoid(1.0 / min(minimals)) - 1
        total_similarity +=  similarity

    return total_similarity / (len(categories) - 1)

# 抽样选取最大和最小距离
def Sampling(original_features):
    total_number = len(original_features)
    ids = original_features.keys()
    max = min = 0
    i = 0
    while i < Sampling_Number:
        a = random.randint(0,total_number-1)
        b = random.randint(0,total_number-1)
        while b == a:
            b = random.randint(0,total_number-1)
        if max == min == 0:
            min = dist.distance(original_features[ids[a]],original_features[ids[b]])
            max = min
        else:
            new_distance = dist.distance(original_features[ids[a]],original_features[ids[b]])
            if max < new_distance:
                max = new_distance
            if min > new_distance:
                min = new_distance
        i += 1
    return max,min

#　代表性子集的代表性衡量
def metric(origin_features,profile_features):
    category_number = len(datapre.category_dic)
    total_number = len(origin_features.keys())
    # 一共分为三个部分,属性损耗,分布损耗,代表性子集差异性
    max,min = Sampling(origin_features)
    loss1 = ((AttributeLoss(origin_features,profile_features)) - total_number * min) / (total_number * max - total_number * min)
    loss2 = DistributionLoss(origin_features,profile_features) / math.sqrt(category_number)
    loss3 = Dissimilarity(profile_features) / category_number
    print loss1,loss2,loss3
    loss = loss1 + loss2 + loss3
    return loss

def test():
    features = datapre.Features()
    profile_features = {}
    i = 0
    for key in features.keys():
        profile_features[key] = features[key]
        i += 1
        if i > 20:
            break
    print metric(features,profile_features)
test()