#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import pickle
import numpy as np

# 加载资源
class Resource:
    def __init__(self,categories):
        self.Repre = {}
        # 一次性加载代表性矩阵和id字典
        for category in categories:
            self.Repre[category] = np.load("new%sRepresentativeMatrix.npy" % category)
        self.Repre_id = {}
        for category in categories:
            open_file = open("new%sRepresentativeDictionary.pickle" % category)
            self.Repre_id[category] = pickle.load(open_file)
            open_file.close()