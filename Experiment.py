#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DBSCAN_Clustering as dbscan
import DataPrepare as pre
import time

def run():
    # 数据准备
    features = pre.Features("StandardUsers")

    # 聚类
    starttime = time.time()
    # 使用dbscan算法聚类
    results = dbscan.Cluster(features)
    endtime = time.time()
    print "cost %f seconds" % (endtime - starttime)

run()