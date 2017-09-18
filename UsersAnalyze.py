#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os

methods = ["GB","kmedoids","sa"]
# 汇总所有方法提取出的代表性用户,计算他们的交集
path = "/home/duncan/TwitterDataSets/6W/"

# 读取在alpha等于某个值时某一个方法在某个领域阈值下的提取的所有代表性用户
def ReadProfilesByMethod(method,epsilon,alpha):
    profiles = []
    newpath = path + alpha + "/" + "epsilon=" + epsilon
    files = os.listdir(newpath)
    for file in files:
        if file[0] == method[0]:
            with open(newpath + "/" + file,"r") as f:
                lines = f.readlines()
            temp_profiles = lines[1].lstrip().rstrip().split("\t")
            profiles += temp_profiles
    profiles = set(profiles)
    # print profiles
    return profiles

def test(alpha):
    epsilons = ["0.1555","0.1556","0.1560"]
    GB_profiles = set()
    kmedoids_profiles = set()
    sa_profiles = set()
    for epsilon in epsilons:
        GB_profiles = GB_profiles | ReadProfilesByMethod("GB",epsilon,alpha)
        kmedoids_profiles = kmedoids_profiles | ReadProfilesByMethod("kmedoids",epsilon,alpha)
        sa_profiles = sa_profiles | ReadProfilesByMethod("sa",epsilon,alpha)
    # read results of PageRank
    with open("/home/duncan/InfluenceTop100","r") as f:
        lines = f.readlines()
    results = []
    for line in lines:
        results.append(line.split(" ")[0])
    page_profiles = set(results)
    # intersection
    intersection = kmedoids_profiles & GB_profiles & sa_profiles & page_profiles
    print intersection
test("1.5")

