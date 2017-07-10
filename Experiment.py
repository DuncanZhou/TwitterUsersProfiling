#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import DBSCAN_Clustering as dbscan
import Hierarchical_Clustering as hiec
import KMeans_Clustering as kmeans
import EM_Clustering as em
import LocalSearch as ls
import Recursion_Clustering as rcluster
import Metric
import Select
import Distance as dist
import time
import math

# 惩罚值参数设置

features = datapre.Features()



# 实验运行
def run():
    # 聚类
    starttime = time.time()
    # 使用dbscan算法聚类
    # method = dbscan.DBSCANCluster()
    # 使用层次聚类算法
    # method = hiec.HierarchicalCluster()

    # 使用修改版的k-means聚类
    # method = kmeans.KMeansCluster()
    # results,means_vector = method.Cluster()
    # profile_data = Select.Select1(results,means_vector)

    # 使用EM聚类
    # method = em.EMCluster()
    # # 得到聚类结果
    # results,k_seeds = method.Cluster()
    # profile_data = Select.Select3(k_seeds)

    # 均值搜索
    # profile_data = Select.Select2(range(9))

    # 使用局部搜索算法
    # localsearch = ls.LocalSearch()
    # profile_data = localsearch.Search()

    #　使用递归聚类方法
    method = rcluster.Recursion_Cluster()
    profile_data = method.Search()

    print "代表性子集为:"
    print profile_data.keys()

    # 测试代表性
    representation_loss = Metric.metric(features,profile_data)
    print representation_loss
    endtime = time.time()
    print "cost %f seconds" % (endtime - starttime)

run()