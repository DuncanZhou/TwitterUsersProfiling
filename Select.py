#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre

features = datapre.Features()
# 选择子集算法
def Select1(cluster,means_vector):
    '''

    :param cluster: 聚类结果
    :return: 返回profiledata
    '''
    # 方法一: 从聚类结果中找到近圆心的向量
    profile_data = {}
    i = 0
    # 在每个聚类簇中寻找和均值向量最近的元素作为profile data返回
    while i < len(cluster):
        to_add_userid = cluster[i].pop()
        to_add_vector = features[to_add_userid]
        print means_vector[i]
        min = dist.distance(to_add_vector,means_vector[i])
        for userid in cluster[i]:
            if dist.distance(features[userid],means_vector[i]) < min:
                to_add_userid = userid
                to_add_vector = features[userid]
        profile_data[to_add_userid] = to_add_vector
        i += 1
    return profile_data

# 方法二: 启发式搜索
