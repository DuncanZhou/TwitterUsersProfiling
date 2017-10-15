#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''


# split each attribute and argmax the sumarization of the representativeness of all attributes

import math
import Distance as dist
import TwitterWithNeo4j as neo4j
import Metric as metric

# 每个样本的格式[Followers,Activity,Influence,following,location,category,Interests_tags,userid]

# 对该算法做以下改进,在贪心过程中保证使得领域的分布和原来分布相同


# sigmoid函数,挤压函数
def sigmoid(x):
    return 1 * 1.0 / (1 + math.exp(-x))

# define the representativeness between users
def Repre(alpha,u,v):
    # include relationship, influence, activity, interest_tags
    if u == v:
        return 1
    if u[5] != v[5]:
        return 0
    distance = dist.distance(u, v)
    return (2 * sigmoid(1.0 / distance) - 1) * alpha

# split users according to "location" & "category"
def Split(parameters,features):
    check = [4,5]
    # store the results
    users = {}
    for feature in features:
        for i in check:
            if feature[i] not in users.keys():
                temp = set()
                temp.add(feature[7])
                users[feature[i]] = temp
            else:
                users[feature[i]].add(feature[7])
    return users

# get the following
def getFollowing(driver,session,u):
    return neo4j.GetFollowings(u)

# search profiles
def Search(features,categories,users,alpha,epsilon,k,beta):
    driver,session = neo4j.Conn()
    numbers = {}
    # add two constraints when searching
    profiles = set()
    ignore = set()
    while len(profiles) < k:
        for feature in features:
            followings = getFollowing(driver,session,feature[7])
            results = {}
            if feature[7] in ignore:
                continue
            # check the feature whether domain typical or not
            if not metric.checkOneTypical(features,feature[7],profiles,epsilon):
                ignore.add(feature[7])
                continue
            # add the element argmaxTotalRepresentativenss
            # calculate the total representativeness
            total = 0
            for key in users.keys():
                if key in (set(categories.keys()) - set(feature[5])):
                    continue
                sum = 0
                # calculate the total representativenss in each group
                for element in users[key]:
                    if element in followings:
                        sum += alpha * Repre(alpha,feature,features[element])
                    else:
                        sum += Repre(alpha,feature,features[element])
                total += math.pow(sum,beta) * len(users[key])
            results[feature[7]] = total
        # check the domain distribution
        results = sorted(results.items(), key= lambda key:key[1], reverse = True)
        flag = False
        while flag:
            for result in results:
                category = features[result[0]][5]
                if category not in numbers.keys():
                    profile = result[0]
                    numbers[category] = 1
                    break
                elif numbers[category] < (int)(k * categories[category]) + 1:
                    profile = result[0]
                    numbers[category] += 1
                    break
        profiles.add(profile)
        ignore.add(profile)
        print "代表性子集大小为%d" % len(profiles)
    return profiles
