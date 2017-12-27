#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import numpy as np
import copy

best = 0
best_selected = []
def Assignment(M,selected,index,visited,sum):
    global best,best_selected
    '''

    :param M: Matrix待分配矩阵
    :param selected: 选择的列号
    :param index: 当前索引
    :return:
    '''
    if(index == len(M)):
        if sum > best:
            best_selected = copy.copy(selected)
            best = sum
        return

    for j in xrange(M.shape[1]):
        # 没有取过
        if visited[j] == True:
            visited[j] = False
            selected[index] = j
            Assignment(M,selected,index+1,visited,sum + M[index,j])
            visited[j] = True
            selected[index] = -1

if __name__ == '__main__':
    M = np.matrix([[3,1,0],[0,2,7],[4,5,6]])
    best = 0
    selected = [-1 for i in xrange(len(M))]
    visited = [True for i in xrange(M.shape[1])]
    Assignment(M,selected,0,visited,0)
    print best_selected