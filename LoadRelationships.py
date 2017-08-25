#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import os
import DataPrepare as datapre
# 将用户结点之间的关系处理成CSV文件,在批量导入neo-4j中

def LoadToCSV(path):
    users = datapre.GetUsersId()
    files = os.listdir(path)
    ids = map(lambda file:file.replace(".txt",""),files)
    with open("/home/duncan/relationships.csv",mode="wb") as f:
        # 写入csv的头
        f.write(":START_ID(userid)")
        f.write(" ")
        f.write(":END_ID(userid)")
        f.write("\n")
        count = 0
        for id in ids:
            friends = set()
            with open(path + id + ".txt","rb") as subf:
                lines = subf.readlines()
                for line in lines:
                    current_friends = set(line.split(" "))
                friends = friends | (current_friends & users)
            # 获取到该id所有的friends,写入到文件中
            for friend in friends:
                f.write(id)
                f.write(" ")
                f.write(friend)
                f.write("\n")
            count += 1
            print "finished %d users" % count

LoadToCSV("/home/duncan/friends/")



