#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import TwitterWithNeo4j as neo4j
import DataPrepare as datapre
import os

# 创建结点
def CreateNodes(path):
    '''

    :param path: CSV文件路径
    :return:
    '''
    neo4j.CreateNodesFromCSV(path)

# 删除所有结点和关系
def DeleteNodesAndRels():
    neo4j.DeleteAllNodesAndRels()

# 初始化操作
def Initial(path="file:///10w_users.csv"):
    '''
    :param path: csv路径
    :return:
    '''
    # csv文件需要放在默认import目录下
    CreateNodes(path)

    # 建立索引
    neo4j.IndexBySName()

    # 设置userid为唯一
    neo4j.UniqueID()

# 查询两个用户是否有follows关系
def isFollow(userid1,userid2):
    return neo4j.isFollow(userid1,userid2)

# 单条插入关系
def InsertFollowsRel(userid1,userid2):
    neo4j.InsertFollowsRel(userid1,userid2)

# 查询某用户的关联用户,深度不小于7(默认参数=1)
def SearchFollowersByDepth(userid):
    users = neo4j.SearchFollowersByDepth(userid)
    return users

# 查询某个领域内的用户
def SearchUsersByCategory(categroy):
    users = neo4j.SearchUsersByCategory(categroy)
    return users

# 读取文本中该用户follow的id,并且这些id都在数据集中
def GetUserFollowing(path,total_users):
    # total_users 是一个集合
    # 打开一个文件,读取其中该用户所有关注的用户
    results = set()
    with open(path,"rb") as f:
        lines = f.readlines()
        for line in lines:
            ids = set(line.split(" "))
            results = results | (ids & total_users)
    return results

# 对文件夹下的用户建立关系
def InsertFollowsFromFiles(path,total_users):
    # 先读取path下的文件名
    files = os.listdir(path)
    ids = map(lambda file:file.replace(".txt",""),files)
    print "共计%d个用户" % len(ids)
    # 对每个id进行读取其follows的id,然后插入到neo-4j中
    with open("/home/duncan/has_insert.txt","wb") as f:
        has_insert = set(ids[:238])
        for id in has_insert:
            f.write(id)
            f.write("\n")

        count = len(has_insert)
        for id in ids:
            if id in has_insert:
                continue
            results = GetUserFollowing(path + "/" + id + ".txt",total_users)
            print "需要插入%d条关系" % len(results)
            # 插入到图数据库中
            for result in results:
                InsertFollowsRel(id,result)
                # print "插入%d条关系" % number
            count += 1
            f.write(id)
            f.write("\n")

            print "共%d个用户,已完成%d个用户" % (len(ids),count)



# 从mysql数据库中将标准人物样本库的人物关系存入neo4j中
# mysql数据格式:userid1,userid2,followed_by,following
# def InsertRelsToNeoFromMysql(table="relation_temp"):
#     relationships = mysql.getUserRelation(table)
#     print len(relationships)
#     # 对每一条关系插入到neo4j中
#     count = 0
#     for relation in relationships:
#         InsertFollowsRel(relation[0],relation[1])
#         count += 1
#         print "insert %d relations" % count


if __name__ == '__main__':
    pass
    # 初始化操作,最开始执行一次,用于创建结点
    # DeleteNodesAndRels()
    # Initial()
    # 根据id建立索引
    # neo4j.IndexByID()

    # 2017.8.24 16:40开始
    # users = datapre.GetUsersId()
    # InsertFollowsFromFiles("/home/duncan/friends/",users)
    # 插入mysql中所有的关系
    # InsertRelsToNeoFromMysql()
