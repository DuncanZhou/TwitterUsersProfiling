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
# 一共分为三个部分,属性损耗,分布损耗,代表性子集差异性

original_features = datapre.Features()
people = datapre.People(original_features)
# 计算一个结点对另一个节点的代表性
def Repre(u,v):
    if u == v:
        return 1

    distance = dist.distance(u,v)
    return 2*sigmoid(1.0 / distance) - 1

# sigmoid函数,挤压函数
def sigmoid(x):
    return 1 * 1.0 / (1 + math.exp(-x))

# 某个具体领域代表性计算
def AttributeRepresentativeByDomain(profiles,domain):
    original_domain = people[domain]
    profile_domain = [id for id in profiles if original_features[id][5] == domain]
    # repre = 0
    # for key in original_domain:
    #     repre += max(Repre(original_features[u],original_features[key]) for u in profile_domain)
    repre = sum(max(Repre(original_features[u],original_features[key]) for u in profile_domain) for key in original_domain)
    return repre + len(profile_domain)

# 属性代表性
def AttributeRepresentative(profiles):
    # 分别在每个领域内计算代表性
    # for category in categories:
    #     tuples = people[category]
    #     # 得到profiles中在这领域的代表性用户
    #     profile_domain = [id for id in profiles if origin_features[id][5] == category]
    #     if len(profile_domain) != 0:
    #         repre += AttributeRepresentativeByDomain(origin_features,profile_domain,tuples,category)
    # return repre
    repre = sum(max(Repre(original_features[u],original_features[key]) for u in profiles) for key in original_features.keys())
    return repre + len(profiles)

# 领域分布损耗
def DistributionLoss(profiles):
    categories = {}
    for key in original_features.keys():
        if original_features[key][5] not in categories.keys():
            categories[original_features[key][5]] = 1
        else:
            categories[original_features[key][5]] += 1
    for key in categories.keys():
        categories[key] = categories[key] * 1.0 / len(original_features)

    profile_categories = {}
    for key in profiles:
        if original_features[key][5] not in profile_categories.keys():
            profile_categories[original_features[key][5]] = 1
        else:
            profile_categories[original_features[key][5]] += 1

    for key in profile_categories.keys():
        profile_categories[key] = profile_categories[key] * 1.0 / len(profiles)

    # 统计损耗
    loss = 0
    for key in categories.keys():
        if key not in profile_categories.keys():
            loss += 1
        else:
            loss += pow(categories[key] - profile_categories[key],2)
    return math.sqrt(loss)

# 子集内部差异性
def Dissimilarity(profiles):
    # 先将所有人分类
    categories = {}
    for key in profiles:
        if original_features[key][5] not in categories.keys():
            list = [key]
            categories[original_features[key][5]] = list
        else:
            categories[original_features[key][5]].append(key)

    # 只有一个领域的用户
    if len(categories) == 1:
        return 1

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
                    minimals.append(min([dist.distance(original_features[id1],original_features[id2]) for id2 in other]))
                similarity += 2 * sigmoid(1.0 / min(minimals)) - 1
        total_similarity += similarity

    return total_similarity / (len(categories) - 1)

# 相似性
def Similarity(u,v):
    disatance = dist.distance(original_features[u],original_features[v])
    similarity = 2 * sigmoid(1.0 / disatance) - 1
    return similarity

# 检查代表性子集中的单个元素是否满足领域代表性
def checkOneTypical(target,profiles,epsilon):
    categories = set([original_features[key][5] for key in profiles])
    categories = categories - set([original_features[target][5]])
    for category in categories:
        list = [Similarity(target,u) for u in profiles if original_features[u][5] == category]
        # 代表性子集中某个领域没有,继续判断
        if len(list) == 0:
            continue
        if max(list) > epsilon:
            # print max(list)
            return False
    return True

# 检查代表性子集中任意两个领域的相似性是否超出某个阈值
def checkAllTypical(profiles,epsilon):
    '''

    :param origin_features: 原始数据集
    :param profiles:  代表性子集ids
    :param epsilon: 阈值
    :return:
    '''
    for profile in profiles:
        if checkOneTypical(profile,profiles,epsilon) == False:
            return False
    return True

# # 抽样选取最大和最小距离
# def Sampling(original_features):
#     total_number = len(original_features)
#     ids = original_features.keys()
#     max = min = 0
#     i = 0
#     while i < Sampling_Number:
#         a = random.randint(0,total_number-1)
#         b = random.randint(0,total_number-1)
#         while b == a:
#             b = random.randint(0,total_number-1)
#         if max == min == 0:
#             min = dist.distance(original_features[ids[a]],original_features[ids[b]])
#             max = min
#         else:
#             new_distance = dist.distance(original_features[ids[a]],original_features[ids[b]])
#             if max < new_distance:
#                 max = new_distance
#             if min > new_distance:
#                 min = new_distance
#         i += 1
#     return max,min

# 一共分为三个部分,属性损耗,分布损耗,代表性子集差异性
# maxn,minn = Sampling(datapre.Features())
#　代表性子集的代表性衡量
# def metric(origin_features,profiles):
#     category_number = len(datapre.category_dic)
#     total_number = len(origin_features.keys())
#
#     loss1 = ((AttributeLoss(origin_features,profiles)) - total_number * minn) / (total_number * maxn - total_number * minn)
#     loss2 = DistributionLoss(origin_features,profiles) / math.sqrt(category_number)
#     loss3 = Dissimilarity(origin_features,profiles) / category_number
#     loss = loss1 + loss2 + loss3
#     return loss

# def test():
#     features = datapre.Features()
#     profile_features = {}
#     i = 0
#     for key in features.keys():
#         profile_features[key] = features[key]
#         i += 1
#         if i > 20:
#             break
#     print metric(features,profile_features)
# test()