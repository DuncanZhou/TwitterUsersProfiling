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
import Clustering_NN as enn
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

    # 使用局部搜索算法
    # localsearch = ls.LocalSearch()
    # profile_data = localsearch.Search()

    #　使用递归聚类方法
    # method = rcluster.Recursion_Cluster()
    # profile_data = method.Search()

    # 使用聚类后再搜索方法
    method = enn.Clustering_NN()
    profile_data = method.Search()

    print "代表性子集大小为:%d" % len(profile_data.keys())
    for key in profile_data.keys():
        print key + " ==> " + datapre.find_key(datapre.category_dic,features[key][5])

    # 测试代表性
    representation_loss = Metric.metric(features,profile_data)
    print representation_loss
    endtime = time.time()
    print "cost %f seconds" % (endtime - starttime)

run()