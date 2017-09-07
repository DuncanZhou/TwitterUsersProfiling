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
def PaintRepre(A,B,C,D,alpha):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([40,60,80,100])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(8,5))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title(r"$\epsilon$=%.4f" % alpha,fontsize=12,fontweight='bold')    #默认字体大小为12
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

    plt.savefig('%s.pdf' % (str(alpha).replace(".","-")),format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制准确率
def PaintAccuracy(A,B,C,D):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(8,5))
    plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['0.1555','0.1556','0.1560'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title("Accuracy of Classifying(k=100)",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel(r"$\epsilon$ of domain typical",fontsize=13,fontweight='bold')
    plt.ylabel("Accuracy",fontsize=13,fontweight='bold')
    plt.xlim(1,3)         #设置x轴的范围
    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('Accuracy.pdf',format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制准确率
def PaintEpsilon(A,B,C,method):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3,4])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(8,5))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"v",color="blue",label=r"$%s(\epsilon=0.1555)$" % method,linewidth=1.5,linestyle="-.")
    # plt.plot(x,A)
    plt.plot(x,B,">",color="green",label="$%s(\epsilon=0.1556)$" % method,linewidth=1.5,linestyle="--")
    # plt.plot(x,B)
    plt.plot(x,C,"s",color="red",label="$%s(\epsilon=0.1560)$" % method,linewidth=1.5,linestyle="-")
    # plt.plot(x,C)

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title(r"%s under different $\epsilon$" % method,fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("the size of k",fontsize=13,fontweight='bold')
    plt.ylabel("Atrributes Features' Representativeness",fontsize=13,fontweight='bold')
    plt.xlim(1,4)         #设置x轴的范围
    # plt.ylim(43800,48000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('%s.pdf' % method,format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
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

# 绘制领域分布图
def DomainsDistribution(data):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3,4,5,6,7,8,9])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(12,5))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    ax.spines['top'].set_visible(False)  #去掉上边框
    ax.spines['right'].set_visible(False) #去掉右边框
    width = 0.25
    rects1 = ax.bar(x,data[0,:],width,color="y",hatch='/')
    rects2 = ax.bar(x + width,data[1,:],width,color="r",hatch="+")
    rects3 = ax.bar(x + 2 * width,data[2,:],width,color="b",hatch="-")
        # plt.bar(x,A,color="blue",label="original domain distirbution")
        # # plt.plot(x,A)
        # plt.bar(x,B,color="red",label="domain distribution of GB\K-Medoids\SA")
        # # plt.plot(x,B)
        # plt.bar(x,C,color="green",label="domain distribution of PageRank")
    # plt.plot(x,C)

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['Politics','Religion','Military','Education','Economy','Technology','Agriculture','Sports','Entertainment'] #x轴刻度的标识
    plt.xticks(x + 3 * width / 2,group_labels,fontsize=10,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title("Domain Distribution",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("domains",fontsize=13,fontweight='bold')
    plt.ylabel("proportion",fontsize=13,fontweight='bold')
    # plt.xlim(1,9)         #设置x轴的范围
    # plt.ylim(43800,48000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend((rects1[0],rects2[0],rects3[0]),('original','GB\K-Medoids\SA','PageRank'))
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('Distribution.pdf',format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 计算profiles中每个领域分别有多少人
def ProfileDomainDistribution(profiles):
    features = datapre.Features()
    categories = ['Politics','Religion','Military','Education','Economy','Technology','Agriculture','Sports','Entertainment']
    number = [0 for i in range(len(categories))]
    for profile in profiles:
        for i in range(len(categories)):
            if features[profile][5] == categories[i]:
                number[i] += 1
    return number

def Paint():
    # 0.1560
    # A = np.array([37584.537, 38015.656, 38307.095, 38468.860])
    # B = np.array([43507.348, 44922.403, 45761.403, 46271.064])
    # C = np.array([44219.653, 45963.595, 47108.449, 47929.333])
    # D = np.array([25592.255, 25970.675, 29950.690, 30489.681])

    # 0.1556
    # A = np.array([37584.537,38015.656,38307.095,38468.860])
    # B = np.array([43541.673,45055.524,45616.712,46301.794])
    # C = np.array([44174.361,45932.558,47044.142,47882.450])
    # D = np.array([25592.255, 25970.675, 29950.690, 30489.681])

    # 0.1555
    # A = np.array([37583.323,37975.945,38289.485,38436.601])
    # B = np.array([43229.790,44540.790,45283.024,46057.038])
    # C = np.array([43953.424,45642.373,46879.324,47653.545])
    # D = np.array([25592.255, 25970.675, 29950.690, 30489.681])
    # #
    # PaintRepre(A,B,C,D,0.1555)

    # 绘制分类准确性
    # A = [0.319,0.340,0.342]
    # B = [0.338,0.368,0.366]
    # C = [0.387,0.406,0.407]
    # D = [0.239,0.239,0.239]
    # PaintAccuracy(A,B,C,D)

    # 绘制GB在不同阈值下的结果
    # A = [43953.424, 45642.373, 46879.324, 47653.545]
    # B = [44174.361, 45932.558, 47044.142, 47882.450]
    # C = [44219.653, 45963.595, 47108.449, 47929.333]

    # 绘制K-Medoids在不同阈值下的结果
    # A = np.array([43229.790, 44540.790, 45283.024, 46057.038])
    # B = np.array([43541.673, 45055.524, 45616.712, 46301.794])
    # C = np.array([43507.348, 44922.403, 45761.403, 46271.064])

    # 绘制SA在不同阈值下的结果
    A = np.array([37583.323, 37975.945, 38289.485, 38436.601])
    B = np.array([37584.537, 38015.656, 38307.095, 38468.860])
    C = np.array([37584.537, 38015.656, 38307.095, 38468.860])
    PaintEpsilon(A,B,C,"SA")

    # 绘制数据集领域分布
    # DomainDistribution(datapre.CategoriesDistribution())

    # 绘制领域分布图
    # 'Politics','Religion','Military','Education','Economy','Technology','Agriculture','Sports','Entertainment'
    # A = np.array([11934,1888,1299,969,3553,12640,2558,13217,12013])
    # A = A * 1.0 / A.sum(axis=0)
    # B = A
    # with open("/home/duncan/InfluenceTop100","rb") as f:
    #     lines = f.readlines()
    #     profiles = set()
    #     for line in lines:
    #         profiles.add(line.split(" ")[0])
    # C = np.array(ProfileDomainDistribution(profiles))
    # C = C * 1.0 / C.sum(axis=0)
    # data = np.vstack((A,B,C))
    # DomainsDistribution(data)

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
