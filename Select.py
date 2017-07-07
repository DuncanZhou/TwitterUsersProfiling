#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import collections

features = datapre.Features()
# 选择子集算法
def Select1(cluster,means_vector):
    '''

    :param cluster: 聚类结果
    :return: 返回profiledata,类型为字典类型{userid:vector}
    '''
    # 方法一: 从聚类结果中找到近圆心的向量
    profile_data = {}
    i = 0
    # 在每个聚类簇中寻找和均值向量最近的元素作为profile data返回
    while i < len(cluster):
        to_add_userid = cluster[i].pop()
        to_add_vector = features[to_add_userid]
        # print means_vector[i]
        min = dist.distance(to_add_vector,means_vector[i])
        for userid in cluster[i]:
            if dist.distance(features[userid],means_vector[i]) < min:
                to_add_userid = userid
                to_add_vector = features[userid]
        profile_data[to_add_userid] = to_add_vector
        i += 1
    return profile_data

# 方法二: 均值和经验选取
def Select2(to_find):
    # 找出每个category的各个均值,然后找出每个类中和该均值最近的返回
    category_dic = datapre.category_dic
    profile = {}
    for i in to_find:
        sum_fratio = 0
        sum_activity = 0
        sum_influence = 0
        interests = []
        location = []
        count = 0
        for userid in features.keys():
            if features[userid][5] == i:
                sum_fratio += features[userid][0]
                sum_activity += features[userid][1]
                sum_influence += features[userid][2]
                for interest in features[userid][3]:
                    interests.append(interest.lower())
                location.append(features[userid][4])
            count += 1
        interets_tags = dict(collections.Counter(interests))
        location = sorted(dict(collections.Counter(location)).items(),key = lambda x:x[1],reverse=True)[0][0]
        new_interst = map(lambda x:x[0],sorted(interets_tags.items(),key = lambda interest_tags:interest_tags[1],reverse=True)[:10])
        mean_vector = (sum_fratio / count,sum_activity / count,sum_influence / count,new_interst,location,i)
        # 找到均值向量后,在某类中找出距离其最小的样本
        id = features.keys()[0]
        min = dist.distance(mean_vector,features[id])
        for userid in features.keys():
            if features[userid][5] == i and dist.distance(mean_vector,features[userid]) < min:
                id = userid
                min = dist.distance(mean_vector,features[userid])

        # 将其加入代表性子集
        profile[id] = features[id]
    return profile

# 根据id搜寻,返回字典形式
def Select3(k_seeds):
    profile = {}
    for seed in k_seeds:
        profile[seed] = features[seed]
    return profile


