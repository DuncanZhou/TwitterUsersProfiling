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
import time
# 绘制实验结果图

# -*- coding: utf-8 -*-
# 绘制每个方法的属性代表性
def PaintRepre(A,B,C,D,epsilon,alpha):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([40,60,80,100])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,6))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12) #默认字体大小为10
    plt.yticks(fontsize=12)
    plt.title(r"$\epsilon$=%.4f,$\alpha$=%.1f" % (epsilon,alpha),fontsize=12)    #默认字体大小为12
    plt.xlabel("the size of k",fontsize=13)
    plt.ylabel(r"Representativeness($R$(S))",fontsize=13)
    plt.xlim(40,100)         #设置x轴的范围
    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0,ncol=2,fancybox=True)
    # plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12) #设置图例字体的大小和粗细

    plt.savefig('%s-%s.pdf' % (str(epsilon).replace(".","-"),str(alpha).replace(".","-")),format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制准确率(Against epsilon)
def PaintAccuracyAgainstEp(A,B,C,D,alpha):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3])
    # x= np.array([1,2,3,4])
    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,6))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    # group_labels=['40','60','80','100'] #x轴刻度的标识
    group_labels=['0.1555','0.1556','0.1560'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12) #默认字体大小为10
    plt.yticks(fontsize=12)
    # plt.title(r"$\epsilon$=%.4f" % epsilon,fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.title(r"Accuracy of Classifying($\alpha=%.1f,k=100$)" % alpha,fontsize=13)    #默认字体大小为12
    plt.xlabel(r"$\epsilon$",fontsize=20)
    plt.ylabel("Accuracy",fontsize=13)
    # plt.xlim(1,4)         #设置x轴的范围
    plt.xlim(1,3)         #设置x轴的范围

    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0,ncol=2,fancybox=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12) #设置图例字体的大小和粗细

    # plt.savefig('%.4fAccuracy.pdf' % epsilon,format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.savefig('Accuracy%.1f.pdf' % alpha,format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制准确率(against k)
def PaintAccuracyAgainstK(A,B,C,D,epsilon,alpha):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x= np.array([1,2,3,4])
    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,6))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    # ax = plt.gca()
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12) #默认字体大小为10
    plt.yticks(fontsize=12)
    plt.title(r"$\epsilon=%.4f,\alpha=%.1f$" % (epsilon,alpha),fontsize=13)
    plt.xlabel(r"the number of $k$",fontsize=13)
    plt.ylabel("Accuracy",fontsize=13)
    plt.xlim(1,4)         #设置x轴的范围

    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0,ncol=2,fancybox=True)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12) #设置图例字体的大小和粗细

    plt.savefig('%.4f-%.1fAccuracy.pdf' % (epsilon,alpha),format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# against epsilon
def PaintEpsilon(A,B,C,method):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    x = np.array([1,2,3,4])

    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(10,6))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"v",color="blue",label=r"$%s(\epsilon=0.1555)$" % method,linewidth=1.5,linestyle="-.")
    # plt.plot(x,A)
    plt.plot(x,B,">",color="green",label="$%s(\epsilon=0.1556)$" % method,linewidth=1.5,linestyle="--")
    # plt.plot(x,B)
    plt.plot(x,C,"s",color="red",label="$%s(\epsilon=0.1560)$" % method,linewidth=1.5,linestyle="-")
    # plt.plot(x,C)

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12) #默认字体大小为10
    plt.yticks(fontsize=12)
    plt.title(r"$\alpha$=0.6,%s under different $\epsilon$" % method,fontsize=12)    #默认字体大小为12
    plt.xlabel("the size of k",fontsize=13)
    plt.ylabel(r"Representativeness($R$(S))",fontsize=13)
    plt.xlim(1,4)         #设置x轴的范围

    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('%s.pdf' % method,format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
    plt.show()

# 绘制领域分布图
def DomainDistribution(categories):
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
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框
    width = 0.25
    rects1 = ax.bar(x+ width,categories.values(),width,color="g")
    # plt.bar(x,A,color="blue",label="original domain distirbution")
    # # plt.plot(x,A)
    # plt.bar(x,B,color="red",label="domain distribution of GB\K-Medoids\SA")
    # # plt.plot(x,B)
    # plt.bar(x,C,color="green",label="domain distribution of PageRank")
    # plt.plot(x,C)

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels = categories.keys()
    plt.xticks(x + width * 1.5,group_labels,fontsize=10) #默认字体大小为10
    plt.yticks(fontsize=12)
    plt.title("Domain Distribution",fontsize=12)    #默认字体大小为12
    for a,b in zip([c for c in x],categories.values()):
        plt.text(a + width * 1.5,b + 0.08,b,ha="center",va="bottom",fontsize=12)
    plt.xlabel("domains",fontsize=13)
    plt.ylabel("the number of users",fontsize=13)
    # plt.xlim(1,9)         #设置x轴的范围
    # plt.ylim(43800,48000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    # leg = plt.gca().get_legend()
    # ltext = leg.get_texts()
    # plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('OriginalDistribution.pdf',format='pdf')  #建议保存为svg格式，再用inkscape转为矢量图emf后插入word中
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
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框
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
    plt.xticks(x + 3 * width / 2,group_labels,fontsize=10) #默认字体大小为10
    plt.yticks(fontsize=12)
    plt.title("Domain Distribution",fontsize=12)    #默认字体大小为12
    plt.xlabel("domains",fontsize=13)
    plt.ylabel("proportion",fontsize=13)
    # plt.xlim(1,9)         #设置x轴的范围
    # plt.ylim(43800,48000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend((rects1[0],rects2[0],rects3[0]),('original','GB\K-Medoids\SA','PageRank'))
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12) #设置图例字体的大小和粗细

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

# 绘制时间复杂度
def TimeComplexityAgainstK(A,B,C,D,epsilon):
    plt.rcParams['font.sans-serif']=['Arial']  #如果要显示中文字体，则在此处设为：SimHei
    plt.rcParams['axes.unicode_minus']=False  #显示负号

    # x = np.array([1,2,3])
    x= np.array([1,2,3,4])
    #label在图示(legend)中显示。若为数学公式，则最好在字符串前后添加"$"符号
    #color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    #线型：-  --   -.  :    ,
    #marker：.  ,   o   v    <    *    +    1
    plt.figure(figsize=(8,5))
    # plt.grid(linestyle = "--")      #设置背景网格线为虚线
    ax = plt.gca()
    # ax.spines['top'].set_visible(False)  #去掉上边框
    # ax.spines['right'].set_visible(False) #去掉右边框

    plt.plot(x,A,"*",color="green",label="SA",linewidth=1.5,linestyle="-")
    plt.plot(x,B,"p",color="blue",label="K-Medoids",linewidth=1.5,linestyle="--")
    plt.plot(x,C,"s",color="red",label="GB",linewidth=1.5,linestyle="-")
    plt.plot(x,D,"<",color="black",label="PageRank",linewidth=1.5,linestyle="-.")

    # plt.plot(x,D,"--",label="PageRank",linewidth=1.5)
    # plt.plot(x,C,"g^")

    group_labels=['40','60','80','100'] #x轴刻度的标识
    # group_labels=['0.1555','0.1556','0.1560'] #x轴刻度的标识
    plt.xticks(x,group_labels,fontsize=12,fontweight='bold') #默认字体大小为10
    plt.yticks(fontsize=12,fontweight='bold')
    plt.title(r"$\epsilon$=%.4f" % epsilon,fontsize=12,fontweight='bold')    #默认字体大小为12
    # plt.title("Accuracy of Classifying",fontsize=12,fontweight='bold')    #默认字体大小为12
    plt.xlabel("the number of k",fontsize=13,fontweight='bold')
    plt.ylabel("Time(s)",fontsize=13,fontweight='bold')
    plt.xlim(1,4)         #设置x轴的范围
    # plt.ylim(23000,46000)
    #plt.ylim(0.5,1)

    #plt.legend()          #显示各曲线的图例
    plt.legend(loc=0, numpoints=1)
    leg = plt.gca().get_legend()
    ltext = leg.get_texts()
    plt.setp(ltext, fontsize=12,fontweight='bold') #设置图例字体的大小和粗细

    plt.savefig('Time-%.4fAccuracy.pdf' % epsilon,format='pdf')
    plt.show()

# 绘制总的代表性效果图
def PaintTotalRepre(A,B,C,D,alpha):
    epsilons = [0.1555,0.1556,0.1560]
    for epsilon,row in zip(epsilons,range(len(epsilons))):
        PaintRepre(A[row],B[row],C[row],D[row],epsilon,alpha)

# 绘制总的准确率效果图
def PaintTotalAccuracy(A,B,C,D,alpha):
    epsilons = [0.1555,0.1556,0.1560]
    for epsilon,row in zip(epsilons,range(len(epsilons))):
        PaintAccuracyAgainstK(A[row],B[row],C[row],D[row],epsilon,alpha)

def Paint():
    # alpha = 0.4
    # 绘制代表性结果
    # A = [[39317.670,39790.252,40366.054,40831.374],[38832.139,39350.993,40399.873,40845.153],[38832.139,39405.829,40409.946,40873.602]]
    # B = [[44592.917,46209.091,46786.843,47914.210],[44368.051,46369.859,47042.774,47801.642],[44982.317,46167.736,47300.916,48172.758]]
    # C = [[46097.602,48321.697,49677.016,50906.232],[46313.745,48547.211,50096.669,51234.068],[46390.040,48623.506,50181.684,51303.911]]
    # D = [[26283.041,27082.409,31429.368,32147.902],[26283.041,27082.409,31429.368,32147.902],[26283.041,27082.409,31429.368,32147.902]]
    # PaintTotalRepre(A,B,C,D,0.4)

    # 绘制准确率结果
    # A = [[0.315,0.307,0.303,0.296],[0.332,0.338,0.320,0.320],[0.332,0.336,0.327,0.327]]
    # B = [[0.321,0.342,0.319,0.336],[0.331,0.355,0.358,0.361],[0.327,0.351,0.366,0.362]]
    # C = [[0.351,0.362,0.379,0.389],[0.365,0.369,0.390,0.402],[0.365,0.369,0.390,0.403]]
    # D = [[0.176,0.215,0.230,0.239],[0.176,0.215,0.230,0.239],[0.176,0.215,0.230,0.239]]
    # PaintTotalAccuracy(A,B,C,D,0.4)

    # A = [0.296,0.320,0.327]
    # B = [0.336,0.361,0.362]
    # C = [0.389,0.402,0.403]
    # D = [0.239,0.239,0.239]
    # PaintAccuracyAgainstEp(A,B,C,D,0.4)

    # alpha = 0.6
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
    # PaintRepre(A,B,C,D,0.1560,0.6)

    # 绘制分类准确性(against epsilon)
    # A = [0.319,0.340,0.342]
    # B = [0.338,0.368,0.366]
    # C = [0.387,0.406,0.407]
    # D = [0.239,0.239,0.239]
    # PaintAccuracyAgainstEp(A,B,C,D,0.6)

    # 绘制GB在不同阈值下的结果
    # A = [43953.424, 45642.373, 46879.324, 47653.545]
    # B = [44174.361, 45932.558, 47044.142, 47882.450]
    # C = [44219.653, 45963.595, 47108.449, 47929.333]

    # 绘制K-Medoids在不同阈值下的结果
    # A = np.array([43229.790, 44540.790, 45283.024, 46057.038])
    # B = np.array([43541.673, 45055.524, 45616.712, 46301.794])
    # C = np.array([43507.348, 44922.403, 45761.403, 46271.064])

    # 绘制SA在不同阈值下的结果
    # A = np.array([37583.323, 37975.945, 38289.485, 38436.601])
    # B = np.array([37584.537, 38015.656, 38307.095, 38468.860])
    # C = np.array([37584.537, 38015.656, 38307.095, 38468.860])
    # PaintEpsilon(A,B,C,"SA")

    # 绘制数据集领域分布
    # DomainDistribution(datapre.CategoriesDistribution())

    # 绘制分类准确性(against k)
    # epsilon = 0.1555
    # A = [0.320,0.321,0.310,0.319]
    # B = [0.318,0.350,0.342,0.339]
    # C = [0.334,0.368,0.377,0.387]
    # D = [0.176,0.215,0.230,0.239]

    # epsilon = 0.1556
    # A = [0.332,0.322,0.333,0.340]
    # B = [0.343,0.352,0.372,0.368]
    # C = [0.360,0.389,0.400,0.406]
    # D = [0.176,0.215,0.230,0.239]
    #
    # # epsilon = 0.1560
    # A = [0.332,0.322,0.335,0.342]
    # B = [0.349,0.362,0.359,0.374]
    # C = [0.360,0.386,0.401,0.407]
    # D = [0.176,0.215,0.230,0.239]
    #
    # PaintAccuracyAgainstK(A,B,C,D,0.1555)

    # 绘制原集中领域分布
    # DomainDistribution(datapre.CategoriesUsers())
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

    # 绘制时间复杂度
    # epsilon = 0.1555
    # A = [8.119,8.418,8.176,8.376]
    # B = [224.052,200.843,180.963,139.895]
    # C = [182.477,1735.569,1494.784,11457.288]
    # D = [3.92,3.92,3.92,3.92]

    # epsilon = 0.1556
    # A = [8.217,8.417,8.251,9.878]
    # B = [289.346,179.231,151.791,127.804]
    # C = [40.096,154.016,183.975,483.792]
    # D = [3.92,3.92,3.92,3.92]

    # epsilon = 0.1560
    # A = [8.275,8.970,8.478,8.426]
    # B = [196.425,221.924,131.916,138.491]
    # C = [40.243,58.980,71.586,88.046]
    # D = [3.92,3.92,3.92,3.92]
    # TimeComplexityAgainstK(A,B,C,D,0.1560)

    # 绘制准确率
    # A = [[0.298,0.298,0.291,0.296],[0.336,0.337,0.320,0.326],[0.337,0.341,0.321,0.325]]
    # B = [[0.341,0.337,0.355,0.338],[0.318,0.336,0.336,0.361],[0.341,0.361,0.353,0.368]]
    # C = [[0.343,0.346,0.377,0.382],[0.347,0.365,0.383,0.400],[0.347,0.365,0.383,0.403]]
    # D = [[0.176,0.215,0.230,0.239],[0.176,0.215,0.230,0.239],[0.176,0.215,0.230,0.239]]
    # PaintTotalAccuracy(A,B,C,D,0.8)

    A = [0.296,0.326,0.325]
    B = [0.338,0.361,0.368]
    C = [0.382,0.400,0.403]
    D = [0.239,0.239,0.239]
    PaintAccuracyAgainstEp(A,B,C,D,0.8)

def Run():
    features = datapre.Features()
    epsilons = [0.1560,0.1556,0.1555]
    number = [40,60,80,100]
    for epsilon in epsilons:
        for n in number:
            start_time = time.time()
            profile1 = greedy.Greedy(n,features,datapre.CategoriesDistribution(),epsilon).SearchWithReplace()
            end_time = time.time()
            with open("GB%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("cost %f s" % (end_time - start_time))
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile1)))
                f.write("\n")
                for profile in profile1:
                    f.write(profile + "\t")
            start_time = time.time()
            profile2 = kmedoids.KMedoids(n,features,datapre.CategoriesDistribution(),epsilon).Search()
            end_time = time.time()
            with open("kmedoids%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("cost %f s" % (end_time - start_time))
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile2)))
                f.write("\n")
                for profile in profile2:
                    f.write(profile + "\t")
            start_time = time.time()
            profile3 = sa.SAalgo(n,features,datapre.CategoriesDistribution(),epsilon,0.3,10,0.9).Search()
            end_time = time.time()
            with open("sa%d_%.4f" % (n,epsilon),"wb") as f:
                f.write("cost %f s" % (end_time - start_time))
                f.write("Attribute Representativeness is:")
                f.write(str(metric.AttributeRepresentative(features,profile3)))
                f.write("\n")
                for profile in profile3:
                    f.write(profile + "\t")
# Run()
Paint()
