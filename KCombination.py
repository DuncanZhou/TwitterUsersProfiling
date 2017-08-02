#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 计算n个数中的k个组合
import Metric as metric
import DataPrepare as datapre
import copy
import time

class KCombination:
    def __init__(self,array,features):
        self.features = features
        self.array = array
        self.temp = []
        self.result = []
        self.minloss = -1

    def kcombination(self,index,k):
        '''
        :param index: 当前位置
        :param k: 还需加入的个数
        :return:
        '''
        if k == 1:
            # 还需加入一个
            i = index
            while i < len(self.array):
                self.temp.append(self.array[i])
                if self.minloss == -1 or metric.metric(self.features,self.temp) < self.minloss:
                    self.minloss = metric.metric(self.features,self.temp)
                    self.result = copy.deepcopy(self.temp)
                    print self.result
                self.temp.remove(self.array[i])
                i += 1
        else:
            i = index
            while i <= len(self.array) - k:
                self.temp.append(self.array[i])
                self.kcombination(i + 1,k - 1)
                self.temp.remove(self.array[i])
                i += 1

def test():
    starttime = time.time()
    features = datapre.Features()
    array = features.keys()
    kcombination = KCombination(array,features)
    kcombination.kcombination(0,20)
    print kcombination.result
    endtime = time.time()
    print endtime - starttime
test()