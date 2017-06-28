#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Queue as queue
import Distance as dist
import random
import DataPrepare as datapre

class DBSCANCluster:
    def __init__(self):
        # 定义领域参数{e,MinPts}
        self.MinPts = 2
        self.e = 0.9
        self.features = datapre.Features()

    # DBSCAN聚类算法
    def Cluster(self):
        '''

        :param features: 字典格式的特征向量集,格式如{userid:feature}
        :return:
        '''
        # 初始化核心对象集
        omiga = set()
        # 寻找核心对象
        for key1 in self.features.keys():
            # 领域内对象的个数
            count = 0
            # 遍历确定其是否是核心对象
            for key2 in self.features.keys():
                if key1 != key2 and dist.distance(self.features[key1],self.features[key2]) <= e:
                    count += 1
            if count >= self.MinPts:
                omiga.add(key1)
        print "共%d个核心对象" % len(omiga)
        # 初始化聚类簇的个数
        k = 0
        # 初始化当前未访问的样本集合
        to_visit = set(self.features.keys())
        # 开始聚类
        clusters = []
        while len(omiga) > 0:
            # 记录当前为访问集合
            new_to_visit = set(to_visit)
            # 从核心对象中随机取一个,初始化队列
            kernal_object = random.sample(omiga,1)[0]
            Q = queue.Queue()
            Q.put(kernal_object)
            # 移除核心对象
            to_visit -= set(kernal_object)
            while not Q.empty():
                # 出队
                q = Q.get()
                # 检查领域对象个数是否大于MinPts
                count = 0
                neighbor = set()
                for key in self.features.keys():
                    if key != q and dist.distance(self.features[key],self.features[q]):
                        neighbor.add(key)
                        count += 1
                if count >= self.MinPts:
                    temp = neighbor & to_visit
                    # 将temp中的对象加入队列中
                    for t in temp:
                        Q.put(t)
                    to_visit -= temp
            k += 1
            print "已有%d个聚类簇" % k
            # 当前聚类簇
            cluster = set()
            cluster_objects = new_to_visit - to_visit
            for obs in cluster_objects:
                cluster.add(obs)
            # 加入聚类簇
            clusters.append(cluster)
            omiga -= cluster_objects
            print len(omiga)
        return clusters









