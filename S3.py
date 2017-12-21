#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

class S3:
    def __init__(self,users,features,k):
        # 用户数据
        self.users = users
        # 子集大小
        self.k = k

    # 分组
    def SplitToGroups(self,users):
        pass

    # 定义组代表性
    def GroupR(self,profiles,group):
        pass

    # 定义总的代表性目标函数
    def Q(self):
        pass