#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Initial as init
import Metric
import numpy as np
import math
import time

class S3:
    def __init__(self,users,num,R,k,beta):
        # 用户数据
        self.users = users
        # 子集大小
        self.k = k
        # 平衡参数
        self.beta = beta
        # 代表性矩阵
        self.R = R
        # 总人数
        self.num = num

    # 分组
    def SplitToGroups(self):
        # 按照location分组
        groups = {}
        for i in range(len(self.users)):
            location = self.users.loc[i]['location']
            if location not in groups.keys():
                groups[location] = [i]
            else:
                groups[location].append(i)
        return groups

    # 定义组代表性
    def Q(self,profiles,groups):
        start = time.time()
        profiles_groups = {}
        for i in profiles:
            index = self.users[self.users['userid'] == i].index[0]
            location = self.users.loc[index]['location']
            if location not in profiles_groups.keys():
                profiles_groups[location] = [self.users[(self.users['userid'] == i)].index[0]]
            else:
                profiles_groups[location].append(self.users[(self.users['userid'] == i)].index[0])

        # 对每个group计算P函数值
        Q_score = 0
        for key in profiles_groups.keys():
            cur_group = profiles_groups[key]
            orginal_group = groups[key]
            # 统计cur_group中每个
            temp = self.R[cur_group,:]
            P = np.sum(np.mean(temp[:,orginal_group],axis=0),axis=0)
            Q_score += math.pow(len(groups[key]),self.beta) * math.pow(P,self.beta)
        end = time.time()
        print "计算Q_score花费%fs" % (end - start)
        return Q_score

    # 直接假设已经按照领域划分了group
    def SearchWithNoGroups(self):
        profiles = set()
        results_vector = np.asarray([0 for i in xrange(self.num)])
        while len(profiles) < self.k:
            # 每次选择使得rc最大的加入
            # results = {i:np.sum(np.mean(np.vstack((results_vector,self.R[i])),axis=0),axis=0) / (len(profiles)+1) for i in range(self.num) if i not in profiles}
            results = {i:np.sum(results_vector * len(profiles) + self.R[i],axis=0) / self.num for i in range(self.num) if i not in profiles}
            profiles.add(max(results.items(),key=lambda key:key[1])[0])
            # 更新results_vector
            results_vector = (results_vector * len(profiles) + self.R[i]) / len(profiles)
            # print len(profiles)
        # 将索引转换成用户id
        profiles = [self.users.loc[i]['userid'] for i in profiles]
        return profiles

    # 贪心算法寻找
    def Search(self):
        groups = self.SplitToGroups()
        profiles = set()
        count = 0
        while len(profiles) < self.k:
            results = {self.users.loc[i]['userid']:self.Q(profiles | set([self.users.loc[i]['userid']]),groups) for i in range(len(self.users)) if self.users.loc[i]['userid'] not in profiles}
            # 排序results,保留最大值
            profiles.add(max(results.items(),key=lambda key:key[1])[0])
            count += 1
            print count
        print profiles
        return profiles

def test():
    category = "Sports"
    users,R,id_list,g = init.Init(category)
    metric = Metric.Metrics(users,R,id_list,g)
    num = len(users) * 0.05
    s3 = S3(users,len(users),R,num,0.6)
    start_time = time.time()
    profiles = s3.SearchWithNoGroups()
    end_time = time.time()
    print "cost %f s" % (end_time - start_time)
    rc,rt,rscore = metric.RScore(profiles)
    print "特征代表性:%f,拓扑结构代表性:%f,rscore:%f" % (rc,rt,rscore)

test()