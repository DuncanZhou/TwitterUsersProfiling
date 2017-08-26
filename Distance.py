#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import math
import TwitterWithNeo4j as neo4j

'''使用闵可夫斯基距离和VDM结合,对于用户的兴趣标签采用相似度的倒数来计算距离'''
'''对于数值特征需要将其归一化'''

# 闵可夫斯基距离中的P参数,P为2时,则为欧式距离
P = 2

# 高斯核函数中的sigma
sigma = 1

# 每个样本的格式[Followers/Following,Activity,Influence,Interests_tags,location,category]
# 定义每个特征的权重
weight = [0.16,0.21,0.26,0.16,0.21]
# weight = [0.16,0.16,0.16,0.16,0.16,0.2]

# 距离变小变量
alpha = 0.8

# 距离函数
def distance(feature1,feature2):
    # 非对称函数,求feature1对feature2的代表性损耗
    # 前三个特征属于连续特征,基于闵可夫斯基来计算
    part1 = 0
    for i in range(3):
        part1 += weight[i] * math.pow(feature1[i]-feature2[i],P)

    # Interest_tags基于相似性(Jaccard相似性)来计算
    tags1 = set(map(lambda word:word.lower(),feature1[3]))
    tags2 = set(map(lambda word:word.lower(),feature2[3]))
    part2 = 1 - len(tags1 & tags2) * 1.0 / len(tags1 | tags2)

    # location和category属于离散属性,基于离散属性距离计算
    if feature1[4] == feature2[4]: part3 = 0
    else: part3 = 1
    if feature1[5] == feature2[5]: part4 = 0
    else: part4 = 100
    # distance = math.exp(-1 * 1.0 / (2 * math.pow(sigma,2)) * math.pow(part1 + weight[3] * part2 + weight[4] * part3 + weight[5] * part4,1.0 / P))
    distance = math.pow(part1 + weight[3] * part2 + weight[4] * part3 + part4,1.0 / P)
    # 非对称的距离函数,如果v follows u,那么u对v的距离降低
    if neo4j.CheckFollows(feature2[6],feature1[6]) == True:
        distance *= alpha
    return distance

# def test():
#     feature1 = [0.1,0.1,0.3,set(['a','b','c']),'US','Politics']
#     feature2 = [0.1,0.1,0.3,set(['b','b','c']),'US','Politics']
#     print distance(feature1,feature2)
# test()
