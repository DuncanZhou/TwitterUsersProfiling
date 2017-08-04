#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist
import DataPrepare as datapre
import Metric as metric

class Greedy:
    def __init__(self,k,features,categories):
        '''

        :param k: 共计需要寻找的代表性子集大小
        :param categories: 领域分布
        :param features: 全局特征集
        '''
        self.k = k
        self.features = features
        self.categories = categories

    # 将一个领域内的用户按距离排序
    @staticmethod
    def SortByDistance(ids,features):
        id_dist = {}
        for id1 in ids:
            distance = 0
            for id2 in ids:
                distance += dist.distance(features[id1],features[id2])
            id_dist[id1] = distance

        # 对字典进行排序
        id_dists = sorted(id_dist.items(),key=lambda key:key[1])
        return id_dists

    def Search(self):
        profiles = []
        # 先计算每个领域分别需要的人数,并贪心算法搜索
        categories = {}
        for category in self.categories.keys():
            categories[category] = (int)(self.k * self.categories[category])
            tuples = [id for id in self.features.keys() if self.features[id][5] == category]
            # 返回这个领域最小的前k个
            tuples = Greedy.SortByDistance(tuples,self.features)[:categories[category]]
            for element in tuples:
                profiles.append(element[0])
        return profiles

def test():
    method = Greedy(20,datapre.Features(),datapre.CategoriesDistribution())
    profiles = method.Search()
    for profile in profiles:
        print profile + " " + method.features[profile][5]
    print metric.checkTypical(method.features,profiles,0.0498)
test()




