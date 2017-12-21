#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Metric as metric
import numpy as np
import pandas as pd
import pickle
import networkx as nx

# 初始化代表性矩阵
def Init(category):
    print "加载数据"
    feature = ['followers','friends','statuses','favourites','activity','influence','location','verified']
    id_list_path = "%s_ids" % category
    rels_path = "%s_rels" % category
    users = pd.read_csv(category+"Users.csv")
    R = np.load("%sRepresentativeMatrix.npy" % category)
    ids_file = open(id_list_path,'rb')
    id_list = pickle.load(ids_file)
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    g = nx.Graph()
    g.add_edges_from(rels)
    print "数据加载完毕"
    return feature,users,R,id_list,g



# InitialMatrix(datapre.Features())