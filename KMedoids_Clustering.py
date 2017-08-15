#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# k-mediods,是k-means的一种变体.相较于k-means他不再是简单地选取一个均值作为聚类簇的质点,而是
# 寻找在聚类簇中距离之差之和最小的作为最新质点.同时,因为这样,该算法的复杂度高于k-means

import DataPrepare as datapre
import Distance as dist
import Metric as metric
import time

class KMedoidsCluster:
    def __init__(self,k,datasets):
        # 需要聚类的数据集合
        self.features = datasets
        # 定义最大迭代次数
        self.Max_iteration = 100
        # 定义聚类簇个数
        self.k_min = k

    # 计算质点到其聚类簇中其它点的距离之和
    def CalcDistance(self,clusters,point):
        '''

        :param cluster: cluster为聚类簇,为list类型
        :param point: 质点
        :return: 距离绝对值之和
        '''
        sum = 0
        for seed in clusters:
            sum += dist.distance(self.features[seed],self.features[point])
        return sum

    # 选取新的质点
    def SelectNewMediod(self,clusters):
        results = {}
        for element in clusters:
            results[element] = self.CalcDistance(clusters,element)
        return (min(results.items(),key=lambda key:key[1]))[0]

    # 将人物按领域分类
    def People(self):
        # 将人物按领域分类
        people = {}
        for key in self.features.keys():
            if self.features[key][5] not in people.keys():
                people[self.features[key][5]] = [key]
            else:
                people[self.features[key][5]].append(key)
        return people

    # 聚类
    def Cluster(self):
        k = self.k_min
        # 初始化种子
        k_seeds = list(datapre.Initial(self.features,k))

        # 聚类簇
        cluster = {}

        # 开始迭代
        iteration = 0
        while iteration < self.Max_iteration:
            print k_seeds
            for seed in k_seeds:
                cluster[seed] = set()

            # 对所有元素进行聚类
            for key in self.features.keys():
                results = {}
                for seed in k_seeds:
                    results[seed] = dist.distance(self.features[seed],self.features[key])
                # 距离k_seeds中的id最近,并入id聚类簇中
                id = (min(results.items(),key=lambda key:key[1]))[0]

                # # 计算样本与各均值向量距离,距离最近的向量划入相应的簇
                # min = dist.distance(self.features[key],self.features[k_seeds[0]])
                # # print min
                # i = 1
                # id = 0
                # while i < k:
                #     if dist.distance(self.features[key],self.features[k_seeds[i]]) < min:
                #         min = dist.distance(self.features[key],self.features[k_seeds[i]])
                #         id = i
                #     i += 1
                # 并入该聚类簇中
                new_element = set()
                new_element.add(key)
                cluster[id] = cluster[id] | new_element

            # 更新质点向量
            # flag来判断是否需要停止迭代
            flag = True
            # 对每个聚类簇分别判断
            new_k_seeds = set()
            for seed in k_seeds:
                new_mediod = self.SelectNewMediod(list(cluster[seed]))
                new_k_seeds.add(new_mediod)
                if new_mediod != seed:
                    # 需要继续迭代
                    flag = False

            if flag == True:
                # 停止迭代
                break
            k_seeds = new_k_seeds
            iteration += 1
            print "迭代%d次" % iteration

        return cluster,k_seeds

class KMedoids:
    # 初始函数
    def __init__(self,k,categories,epsilon):
        self.features = datapre.Features()
        # 一共需要人数
        self.k = k
        # 全局领域分布情况
        self.categories = categories
        # 典型性判断参数
        self.epsilon = epsilon

    # 删除多出来的用户
    def Delete(self,profiles):
        # 先统计每个领域的人数,用以统计该领域是否能被减少人数
        categories = datapre.DomainDistribution(profiles,self.features)
        # 遍历,如果将其排除,那么损耗将会减少多少,将排除后损失依然小的排除
        to_delete = len(profiles) - self.k
        has_category = set()
        i = 0
        while i < to_delete:
            loss = {}
            for profile in profiles:
                if self.features[profile][5] in has_category:
                    continue
                profiles.remove(profile)
                loss[profile] = metric.AttributeLoss(self.features,profiles)
                profiles.add(profile)
            # 对loss排个序,把损耗依然小的且可以移除的移除
            to_delete_id = (min(loss.items(),key=lambda dic:dic[1]))[0]
            has_category.add(self.features[to_delete_id][5])
            # 判断是否能删除
            if categories[self.features[to_delete_id][5]] == int(self.categories[self.features[to_delete_id][5]] * self.k) + 1:
                profiles.remove(to_delete_id)
                i += 1
        return profiles

    # 从聚类好的聚类簇中替换不满足要求的元素
    def Replace(self,profiles,cluster):
        '''

        :param profiles: 完成的中心点
        :param cluster: 字典形式的,以profiles为key,聚类簇value为列表格式
        :return: 返回替换好的profiles
        '''
        # 替换过程用离medoids最近的且满足要求的元素来替换
        new_profiles = profiles
        for profile in profiles:
            if not metric.checkOneTypical(self.features,profile,new_profiles,self.epsilon):
                new_profiles.remove(profile)
                # 对profile进行替换,在cluster[profile]寻找距离profile最近,且满足条件的来替换
                results = {}
                for element in cluster[profile]:
                    results[element] = dist.distance(self.features[element],self.features[profile])
                results = sorted(results.items(),key=lambda key:key[1])
                flag = False
                # 在results中找到距离profile最近,且满足领域典型要求的元素
                for key in results.keys():
                    if metric.checkOneTypical(self.features,key,new_profiles,self.epsilon):
                        new_profiles.add(key)
                        cluster[key] = cluster[profile]
                        cluster.pop(profile)
                        flag = True
                        break
                # 没找到领域典型的,需要在原集中取出这部分元素,重新聚类
                if flag == False:
                    pass
        return new_profiles

    # 聚类结束
    def Search(self):
        profiles = set()
        medoids_clusters = {}
        # 对每个领域聚类
        people = datapre.People(self.features)
        for category in self.categories.keys():
            # 对每个领域进行聚类
            number = int(self.k * self.categories[category]) + 1
            tuples = people[category]
            method = KMedoidsCluster(number,datapre.FeaturesById(tuples,self.features))
            clusters,medoids = method.Cluster()
            # 先加入到profiles中
            for medoid in medoids:
                profiles.add(medoid)
                medoids_clusters[medoid] = clusters[medoid]
        print "开始删除"
        # 删除多出来的
        profiles = self.Delete(profiles)
        profiles = self.Replace(profiles,medoids_clusters)
        return profiles



def test():
    start_time = time.time()
    method = KMedoids(30,datapre.CategoriesDistribution(),0.499)
    profiles = method.Search()
    end_time = time.time()
    print metric.AttributeLoss(datapre.Features(),profiles)
    print "cost %f s" % (end_time - start_time)
test()


