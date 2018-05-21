#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import networkx as nx
import pickle

# 先对每个数据集的全部做社区发现,然后持久化每个社区.然后再根据采样率进行聚类,挑选代表性人物

# 先对数据集做社区发现
def CommunityDetectionByNX(id_list_path,rels_path):
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    # ids_file = open(id_list_path,'rb')
    # id_list = pickle.load(ids_file)
    # 社区发现
    print "community detection"
    g = nx.Graph()
    g.add_edges_from(rels)
    community = nx.algorithms.community.girvan_newman(g)
    res = sorted(map(sorted, next(community)))
    print res
    # all_users_graph = open("all_users_grapha","wb")
    # pickle.dump(res,all_users_graph,True)