# TwitterUsersProfiling
从大量Twitter用户中找出有代表性的用户
## 实验步骤
[step1]
1.尝试基于混合属性的聚类方法
2.对聚类方法进行优化,提高效率

[step2]
1.在聚类结果中进行搜索,找出profile子集
2.对搜索过程进行优化,提高效率

[step3]
目前已完成的对比方法有:
1.最朴素的LocalSearch
2.先用k-mediods聚类,然后在质点的最近邻进行搜索添加代表性向量,多次迭代

[step4]
下一步:
完成Affinity Propagation的方法
阅读矩阵求解方法


8-17日更新
[提出的方法]
先贪心算法+回溯法(减枝)

[对比方法]
局部搜索算法(LocalSearch),启发式算法(SA),聚类算法(k-medoids),PageRank

[已完成]
启发式算法,聚类算法,本论文提出方法

[待完成]
PageRank,局部搜索算法

