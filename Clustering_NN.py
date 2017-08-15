#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import DataPrepare as datapre
import EM_Clustering as em
import KMedoids_Clustering as kmediods
import Distance as dist
import Metric as metric

# 此方法先聚类,再找最近邻元素加入
class Clustering_NN:
    def __init__(self):
        # 选择聚类方法
        self.cmethod = em.EMCluster()
        self.cmethod = kmediods.KMediodsCluster()
        self.k_min = 9
        # 定义全局特征向量集
        self.features = datapre.Features()

    def Search(self):
        # 记录已经检查过的元素
        has_checked = set()
        # 初始的聚类集合是全集,为默认设置
        # cluster,k_seeds,seeds_loss = self.cmethod.Cluster()
        cluster,k_seeds = self.cmethod.Cluster()
        s_current = {}
        for seed in k_seeds:
            has_checked.add(seed)
            s_current[seed] = self.features[seed]
        loss_current = metric.metric(self.features,s_current)

        while True:
            old_size = len(s_current)
            # 对于k_seeds中每个在其所在的聚类簇中寻找最近邻居
            for seed,i in zip(k_seeds,range(len(cluster))):
                clusters = list(cluster[i])
                min = dist.distance(self.features[seed],self.features[clusters[0]])
                min_id = clusters[0]
                for id in clusters:
                    if id not in has_checked and dist.distance(self.features[seed],self.features[id]) < min:
                        min = dist.distance(self.features[seed],self.features[id])
                        min_id = id
                # 将最近邻加入看是否能降低loss
                has_checked.add(min_id)
                s_current[min_id] = self.features[min_id]
                if metric.metric(self.features,s_current) > loss_current:
                    s_current.pop(min_id)
                else:
                    # 更新loss_current
                    loss_current = metric.metric(self.features,s_current)

            # 如果集合没有改变,停止迭代
            if len(s_current) == old_size:
                break
        return s_current

