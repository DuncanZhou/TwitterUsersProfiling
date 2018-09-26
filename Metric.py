#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import numpy as np
from networkx.classes.function import all_neighbors

GroundTruth_Path = "./GroundTruth/"

class Metrics:
    def __init__(self,users,R,g):
        # 用户数据
        self.users = users
        # 用户总个数
        self.num = len(users)
        # 代表性矩阵
        self.R = R
        # 在图中对应的节点编号
        # 关系图
        self.g = g
        # 转换一下索引结构
        self.index = {userid: users[users.userid == userid].index[0] for userid in users.userid}


    # 根据pandas里的索引返回对应的userid
    def GetID(self,profiles):
        return list(self.users.loc[profiles]['userid'])

    # 获得用户的邻居
    def GetNeighbours(self,u):
        if str(u) in self.g:
            return set([int(i) for i in all_neighbors(self.g,str(u))])
        else:
            return set()

    # 计算特征代表性
    def Rc(self,users,profiles):
        '''

        :param users: DataFrame类型
        :param profiles: 代表性候选集
        :param R: 代表性矩阵
        :return: 返回代表性值
        '''
        # 找到profiles对应的index
            # rows.append(users[(users['userid'] == u)].index[0])
        rows = [self.index[u] for u in profiles]
        cols = [self.index[u] for u in users]
        row_matrix = self.R[rows,:]
        # R中找rows中每列最大值
        return np.sum(np.max(row_matrix[:,cols],axis=0)) / len(cols)
        # R中找rows中的每列平均值
        # return np.sum(np.mean(R[rows,:],axis=0),axis=0) / self.num

    # 计算结构代表性
    def Rt(self,profiles):
        # neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,self.id_dic[str(u)])) if self.id_dic[str(u)] in self.g else set() for u in profiles])
        neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,str(u))) if str(u) in self.g else set() for u in profiles])
        # 所有相邻的
        NS = len(neighbours - set(profiles))
        VS = self.num - len(profiles)
        return 1.0 * NS / VS

    # 计算结构代表性
    def Rt(self,users,profiles):
        # neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,self.id_dic[str(u)])) if self.id_dic[str(u)] in self.g else set() for u in profiles])
        neighbours = reduce(lambda x,y:x | y,[set(all_neighbors(self.g,str(u))) if str(u) in self.g else set() for u in profiles])
        # 所有相邻的
        NS = len(neighbours - set(profiles) & set(users))
        VS = len(users)
        return 1.0 * NS / VS

    # 目标函数
    def RScore(self,profiles):
        rc = round(self.Rc(self.users,profiles,self.R),3)
        rt = round(self.Rt(profiles),3)
        return rc,rt,round(2.0 * rc * rt / (rc + rt),3)

    def ReadUsers(self,path):
        with open(path,'r') as f:
            lines = f.read()
            profiles = set(lines.split(","))
            profiles = set([profile.strip() for profile in profiles if len(profile.strip()) != ""])
        return profiles

    # 计算找出的代表性人物的准确率和召回率，以及 F1-score
    def PR(self,profiles,category,alpha,dataset):
        # 读取标注好的代表性人物
        path = GroundTruth_Path + dataset + "/" + category + "/" + str(alpha)
        true_profiles = self.ReadUsers(path)
        p = len(profiles & true_profiles) * 1.0 / len(profiles)
        r = len(profiles & true_profiles) * 1.0 / len(true_profiles)
        f1 = 2 * p * r / (p + r)
        return p,r,f1