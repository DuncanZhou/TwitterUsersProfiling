#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import math

a = 2
b = 50

# sigmoid函数,挤压函数
def sigmoid(x):
    return 1 * 1.0 / (1 + math.exp(-x))

#  属性特征损耗
def AttributeLoss(origin_features,profile_features):
    loss = 0
    for key in origin_features.keys():
        list = [dist.distance(origin_features[key],profile_features[u]) for u in profile_features.keys() if profile_features[u][5] == origin_features[key][5]]
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

    profile_categories = {}
    for key in profile_features.keys():
        if profile_features[key][5] not in profile_categories.keys():
            profile_categories[profile_features[key][5]] = 1
        else:
            profile_categories[original_features[key][5]] += 1
    # 统计损耗
    loss = 0
    for key in categories.keys():
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

    print categories

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
                similarity += min(minimals)
        total_similarity += 1 * 1.0 / len(categories) * similarity

    return total_similarity

#　子集的代表性衡量
def metric(origin_features,profile_features):
    size_profile = len(profile_features.keys())
    total_number = len(origin_features.keys())
    # 一共分为三个部分,
    loss = 0
    return loss


def test():
    features = datapre.Features()
    profile_features = {}
    count = 0
    for key in features.keys():
        profile_features[key] = features[key]
        count += 1
        if count > 30:
            break
    print Dissimilarity(profile_features)
test()