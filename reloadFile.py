#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import pickle
import numpy as np
suffix = "RepresentativeMatrix.pickle"
categories = ["Politics","Religion","Technology","Economy","Agriculture","Education","Sports","Entertainment","Military"]
# 重新把矩阵文件存储为numpy格式
def Reload(path):
    open_file = open(path)
    R = pickle.load(open_file)
    open_file.close()
    R = np.asarray(R)
    # 加载numpy.load(path)
    # 保存
    np.save("new"+path,R)

# 遍历所有的矩阵文件
def ReloadAll(categories):
    count = 0
    for category in categories:
        Reload(category + suffix)
        count += 1
        print "finished %d" % count

if __name__ == "__main__":
    ReloadAll(categories)