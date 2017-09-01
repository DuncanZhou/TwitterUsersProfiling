#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import numpy as np
import matplotlib.pyplot as plt
# 绘制实验结果图

# -*- coding: utf-8 -*-
def paint(A,B,C,alpha):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([40,60,80,100])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,5))
    plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,color="black",label="SA",linewidth=1.5)
    plt.plot(x,A,"v")
    plt.plot(x,B,"k--",label="K-Medoids",linewidth=1.5)
    plt.plot(x,B,"*")
    plt.plot(x,C,color="red",label="GB",linewidth=1.5)
    plt.plot(x,C,"s")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title("alpha=0.1560",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("the number of S",fontsize=13,fontweight='bold')
    plt.ylabel("Atrributes Features' Representativeness",fontsize=13,fontweight='bold')
    plt.xlim(40,100)         #设置x轴的范围
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('%f.svg' % alpha,format='svg')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

A = np.array([36155.215, 36294.611, 36380.243, 36482.351])
B= np.array([42239.482, 43544.929, 44099.377, 44875.519])
C=np.array([42407.925, 43625.682, 44459.971, 45050.774])
paint(A,B,C,0.1560)