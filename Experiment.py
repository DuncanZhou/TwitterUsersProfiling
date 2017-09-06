#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
import numpy as np
import matplotlib.pyplot as plt
import GreedyAlgorithm as greedy
import KMedoids_Clustering as kmedoids
import SAalgo as sa
import DataPrepare as datapre
import Metric as metric
# 绘制实验结果图

# -*- coding: utf-8 -*-
def PaintRepre(A,B,C,alpha):
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

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title("alpha=%.4f" % alpha,fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("the size of k",fontsize=13,fontweight='bold')
    plt.ylabel("Atrributes Features' Representativeness",fontsize=13,fontweight='bold')
    plt.xlim(40,100)         #设置x轴的范围
    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('%.4f.svg' % alpha,format='svg')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制准确率
def PaintAccuracy(A,B,C):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3])

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

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['0.1555','0.1556','0.1560'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title("Accuracy of Classifying(k=100)",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("epsilon of domain typical",fontsize=13,fontweight='bold')
    plt.ylabel("Accuracy",fontsize=13,fontweight='bold')
    plt.xlim(1,3)         #设置x轴的范围
    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('Accuracy.svg',format='svg')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制领域分布图
def DomainDistribution(categories):
    plt.figure(figsize=(20,10))
    xlabel = categories.keys()
    ylabel = categories.values()
    plt.bar([x for x in range(len(xlabel))],ylabel,align="center",facecolor="yellowgreen",edgecolor="white")

    # 设置x轴标注
    plt.xticks([x for x in range(len(xlabel))],xlabel)
    for a,b in zip([x for x in range(len(xlabel))],ylabel):
        plt.text(a,b + 0.05,b,ha="center",va="bottom",fontsize=15)
    plt.xlabel("domain",fontsize=15)
    plt.ylabel("the number of users",fontsize=15)
    plt.show()

def Paint():
    # 0.1560
    # A = np.array([36155.215, 36294.611, 36380.243, 36482.351])
    # B= np.array([42239.482, 43544.929, 44099.377, 44875.519])
    # C=np.array([42407.925, 43625.682, 44459.971, 45050.774])

    # 0.1556
    # A = np.array([36115.215,36234.611,36300.243,36382.351])
    # B = np.array([42133.516,43382.961,44153.486,44735.654])
    # C = np.array([42310.705,43500.846,44286.267,44778.256])
    # D = np.array([24649.941,24810.953,28374.616,28586.507])

    # 0.1555
    # A = np.array([36108.448,36226.438,36238.788,36343.881])
    # B = np.array([42187.129,43215.800,44001.334,44596.935])
    # C = np.array([42074.657,43158.135,44207.511,44789.412])
    # PaintRepre(A,B,C,0.1555)

    # 绘制分类准确性
    A = [0.319,0.340,0.342]
    B = [0.338,0.368,0.366]
    C = [0.387,0.406,0.407]
    PaintAccuracy(A,B,C)

def Run():
    features = datapre.Features()
    epsilons = [0.1560,0.1556,0.1555]
    number = [40,60,80,100]
    for epsilon in epsilons:
        for n in number:
            profile1 = greedy.Greedy(n,features,datapre.CategoriesDistribution(),epsilon).SearchWithReplace()
            with open("GB%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile1)))
                f.write("\n")
                for profile in profile1:
                    f.write(profile + "\t")
            profile2 = kmedoids.KMedoids(n,features,datapre.CategoriesDistribution(),epsilon).Search()
            with open("kmedoids%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile2)))
                f.write("\n")
                for profile in profile2:
                    f.write(profile + "\t")
            profile3 = sa.SAalgo(n,features,datapre.CategoriesDistribution(),epsilon,0.3,10,0.9).Search()
            with open("sa%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile3)))
                f.write("\n")
                for profile in profile3:
                    f.write(profile + "\t")
# Run()
Paint()
