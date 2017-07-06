#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import DBSCAN_Clustering as dbscan
import Hierarchical_Clustering as hiec
import KMeans_Clustering as kmeans
import Select
import Distance as dist
import time
import math

# 惩罚值参数设置
a = 2
b = 2
features = datapre.Features()

#　子集的代表性衡量
def metric(origin_features,profile_features):
    size_profile = len(profile_features.keys())
    total_number = len(origin_features.keys())
    part1 = 0
    for origin in origin_features.keys():
        min = dist.distance(origin_features[origin],profile_features[profile_features.keys()[0]])
        # 在profile中选取到该对象距离最小的值
        for profile in profile_features:
            if dist.distance(origin_features[origin],origin_features[profile]) < min:
                min = dist.distance(origin_features[origin],origin_features[profile])
        part1 += min

    # 第二部分由与profile大小相关的惩罚值函数构成
    part2 = math.pow(a, b * size_profile * 1.0 / total_number)
    loss = part1 + part2
    return loss

# 实验运行
def run():
    # 聚类
    starttime = time.time()
    # 使用dbscan算法聚类
    # method = dbscan.DBSCANCluster()
    # 使用层次聚类算法
    # method = hiec.HierarchicalCluster()
    # 使用修改版的k-means聚类
    method = kmeans.KMeansCluster()
    # 得到聚类结果
    results,means_vector = method.Cluster()

    # 选择得到代表性子集
    profile_data = Select.Select1(results,means_vector)
    # profile_data = Select.Select2(range(9))

    print "代表性子集为:"
    print profile_data.keys()

    # 测试代表性
    representation_loss = metric(features,profile_data)
    print representation_loss
    endtime = time.time()
    print "cost %f seconds" % (endtime - starttime)

run()