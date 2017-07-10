#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import Distance as dist
import Metric as metric
import Queue

# 用局部搜索算法

class LocalSearch:
    def __init__(self):
        # 定义领域范围
        self.neighbour = 0.5
        # 定义全局特征向量集
        self.features = datapre.Features()
        # 定义最小代表性向量个数
        self.k_min = 9

    def Search(self):
        # 随即初始化k_min个向量作为初始代表性向量
        k_seeds = datapre.Initial(self.features,self.k_min)
        has_checked = set()
        queue_set = set()
        s_current = {}
        for seed in k_seeds:
            s_current[seed] = self.features[seed]
            has_checked.add(seed)
        Loss_current = metric.metric(self.features,s_current)
        # 初始化邻居队列
        Q = Queue.Queue()
        for seed in k_seeds:
            for key in self.features.keys():
                # 该向量没有被检查过且属于该邻居
                if key not in has_checked and dist.distance(self.features[seed],self.features[key]) <= self.neighbour:
                    Q.put((key,seed))
                    queue_set.add(key)
        while not Q.empty():
            neighbours = Q.get()
            # 当前检查的代表性向量
            checking_seed = neighbours[1]
            # 待加入的邻居向量
            neighbour = neighbours[0]
            if neighbour in has_checked:
                continue
            # 该邻居向量已经被访问过了
            has_checked.add(neighbour)
            # 将该向量弹出,将新的邻居加入,并检查
            s_current.pop(checking_seed)
            s_current[neighbour] = self.features[neighbour]
            print Loss_current
            if metric.metric(self.features,s_current) < Loss_current:
                # 邻居加入后,使得目标函数降低,s_current不改变,将Q中当前seed的邻居全部移除
                new_Q = Queue.Queue()
                while not Q.empty():
                    temp = Q.get()
                    if temp[1] != checking_seed:
                        new_Q.put(temp)
                Q = new_Q
                # 更新Loss
                Loss_current = metric.metric(self.features,s_current)
                continue
            s_current[checking_seed] = self.features[checking_seed]
            if metric.metric(self.features,s_current) < Loss_current:
                # 将neighbour加入,并将neighbour的neighbour入队
                for key in self.features.keys():
                    if key not in has_checked and dist.distance(self.features[neighbour],self.features[key]) <= self.neighbour:
                        Q.put((key,neighbour))
                # 更新Loss
                Loss_current = metric.metric(self.features,s_current)
                continue
            # 以上两个条件都不满足,则将s_current恢复
            s_current.pop(neighbour)

        return s_current









