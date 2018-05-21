#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import MySQLdb.cursors
import csv
import TwitterWithNeo4j as neo4j
import cPickle as pickle
import networkx as nx
import Initial as init
from networkx.classes.function import all_neighbors
import time
import pandas as pd
import math
import numpy as np

class Twitter_User:
    def __init__(self,userid,followers,friends,statuses,favourites,activity,influence,location,protected,verified,category):
        self.userid = userid
        self.followers = followers
        self.activity = activity
        self.influence = influence
        self.location = location
        self.category = category
        self.friends = friends
        self.statuses = statuses
        self.favourites = favourites
        self.protected = protected
        self.verified = verified

class Weibo_User:
    def __init__(self,id,friends_count,followers_count,statuses_count,favourtites_count,gender,verified,city,urank,category):
        self.friends_count = friends_count
        self.followers_count = followers_count
        self.statuses_count = statuses_count
        self.favourites_count = favourtites_count
        self.gender = gender
        self.verified = verified
        self.city = city
        self.urank = urank
        self.category = category

# 数据库连接
def Connection():
    conn = MySQLdb.connect(
        host= "192.168.131.191",
        port = 3306,
        user= "root",
        passwd= "",
        db = "weibo",
        # host= "127.0.0.1",
        # port = 3306,
        # user= "root",
        # passwd= "123",
        # db = "TwitterUserInfo",

        # 以字典形式返回结果
        cursorclass = MySQLdb.cursors.DictCursor,
    )
    # 全局变量cursor
    cursor = conn.cursor()
    return conn,cursor

# 数据库关闭
def Close(conn,cursor):
    cursor.close()
    conn.commit()
    conn.close()

# 获取所有用户的特征向量
def GetAllUsersFeature(table="users"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s" % table)
    datas = cursor.fetchall()
    users = []
    for data in datas:
        weibo_user = Weibo_User(data['id'],int(data['friends_count']),int(data['followers_count']),int(data['statuses_count']),int(data['favourites_count']),int(data['gender']),int(data['verified']),data['city'],data['urank'],data['category'])
        # users.append(twitter_user)
        users.append((data['id'],int(data['friends_count']),int(data['followers_count']),int(data['statuses_count']),int(data['favourites_count']),int(data['gender']),int(data['verified']),data['city'],data['urank'],data['category']))
    Close(conn,cursor)
    return users

# 获取某个领域的所有用户的特征向量
def GetUsersFeature(category,table="users"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s where category = '%s'" % (table,category))
    datas = cursor.fetchall()
    users = []
    for data in datas:
        # twitter_user = Twitter_User(data['user_id'],int(data['followers_count']),int(data['friends_count']),int(data['statuses_count']),int(data['favourites_count']),float(data['activity']),float(data['influence_score']),data['time_zone'],data['protected'],data['verified'],data['category'])
        # users.append(twitter_user)
        users.append((data['id'],int(data['friends_count']),int(data['followers_count']),int(data['statuses_count']),int(data['favourites_count']),int(data['gender']),int(data['verified']),data['city'],data['urank'],data['category']))
    Close(conn,cursor)
    return users

# 从csv中获取某一领域用户的数据
def GetUsersFromCSV(path="TotalUsers.csv"):
    # path = "users/" + category + path
    data = pd.read_csv(path)
    return data

# 从csv中获取某一领域用户的数据
def GetUsersFromCSVByCategory(category,path="Users.csv"):
    # path = "users/" + category + path
    path = "users/" + category + path
    data = pd.read_csv(path)
    return data

# 得到特征属性
def GetFeatureColumns():
    return ['followers','friends','statuses','favourites','activity','influence','verified']

# 计算两个用户之间的代表性
# u,v为两个用户的userid
def r(u,v):
    dist = np.linalg.norm(np.asarray(u) - np.asarray(v))
    if dist == 0:
        return 1
    else:
        return 2.0 / (1 + math.exp(-1 / dist)) - 1


# 所有用户的信息label encoding后写入csv文件中
def WriteIntoCSV(users):
    with open("/home/duncan/TotalUsers.csv","wb") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['userid','friends','followers','statuses','favourites','gender','verified','city','urank','category'])
        writer.writerows(users)

def WriteIntoCSVByCategory(category):
    users = GetUsersFeature(category)
    with open("users/%sUsers.csv" % category,"wb") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['userid','friends','followers','statuses','favourites','gender','verified','city','urank','category'])
        writer.writerows(users)

def GetRelationships(users,category):
    # driver,session = neo4j.Conn()
    # users = GetUsersFeature(catgegory)
    # id_list = [user[0] for user in users]
    # relationships = []
    # for i in xrange(len(id_list)):
    #     followings = set(neo4j.GetFollowings(driver,session,id_list[i]))
    #     j = i + 1
    #     while j < len(id_list):
    #         if id_list[j] in followings:
    #             relationships.append([i,j])
    #         j += 1
    # rel_file = open("%s_rels" % catgegory,'wb')
    # ids_file = open("%s_ids" % catgegory,'wb')
    # pickle.dump(relationships,rel_file,True)
    # pickle.dump(id_list,ids_file,True)
    # print len(relationships)
    users = GetUserByCategory(users,category)
    conn,cursor = Connection()
    id_list = []
    relationships = []
    i = 0
    while i < len(users):
        id_list.append(users.iloc[i]['userid'])
        i += 1
    ids = set(id_list)
    # 对已加入的点无需再加入
    has = set()
    for id in id_list:
        # 将id关注的结点加入
        cursor.execute("select tuid from relationships where suid = '%s'" % id)
        results = cursor.fetchall()
        if len(results) == 0:
            continue
        else:
            count = 0
            while count < len(results):
                tuid = int(results[count]['tuid'])
                # 加入时需要判断tuid是否在同一个领域内,如果之前已经加入过了则无须再加入了
                if tuid not in ids or tuid in has:
                    count += 1
                    continue
                relationships.append([id,tuid])
                count += 1
        has.add(id)
    Close(conn,cursor)
    rel_file = open("Graph/%s_rels" % category,'wb')
    ids_file = open("Graph/%s_ids" % category,'wb')
    pickle.dump(relationships,rel_file,True)
    pickle.dump(id_list,ids_file,True)
    print len(relationships)

# 得到所有用户的关系
# def GetRelationships():
#     driver,session = neo4j.Conn()
#     users = pd.read_csv("TotalUsers.csv")
#     id_list = users['userid']
#     relationships = []
#     for i in xrange(len(id_list)):
#         followings = set(neo4j.GetFollowings(driver,session,id_list[i]))
#         j = i + 1
#         while j < len(id_list):
#             if id_list[j] in followings:
#                 relationships.append([i,j])
#             j += 1
#     rel_file = open("all_users_rels",'wb')
#     ids_file = open("all_users_ids",'wb')
#     pickle.dump(relationships,rel_file,True)
#     pickle.dump(id_list,ids_file,True)
#     print len(relationships)

# 社区发现
def CommunityDetection(id_list_path,rels_path):
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    ids_file = open(id_list_path,'rb')
    id_list = pickle.load(ids_file)
    # 社区发现
    print "community detection"
    # cnm.fast_newman(id_list,rels,len(id_list),int(len(id_list) * 0.75))

def CommunityDetectionByNX(id_list_path,rels_path):
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    ids_file = open(id_list_path,'rb')
    id_list = pickle.load(ids_file)
    # 社区发现
    print "community detection"
    g = nx.Graph()
    g.add_edges_from(rels)
    # community = list(asyn_fluidc(g,8))
    # cliques = nx.graph_clique_number(g)
    # print len(community)
    community = nx.algorithms.community.girvan_newman(g)
    res = sorted(map(sorted, next(community)))
    print res
    all_users_graph = open("all_users_grapha","wb")
    pickle.dump(res,all_users_graph,True)

def Communities():
    categories = ["Politics","Sports","Military","Entertainment","Agriculture","Technology","Economy","Education","Religion"]
    # for category in categories:
    #     GetRelationships(category)
    category = "Religion"
    # CommunityDetection("%s_ids" % category,"%s_rels" % category)
    start_time = time.time()
    CommunityDetectionByNX("Graph/%s_ids" % category,"Graph/%s_rels" % category)
    end_time = time.time()
    print "cost %f seconds" % (end_time - start_time)


def repre(users,index,feature):
    rows_num = len(users.index)
    row = np.array(users.iloc[index][feature]).astype(float)
    rows = np.tile(row,(rows_num,1)).astype(float)
    d = np.asarray(users[feature])
    #     temp = np.sum((rows - d) ** 2,axis=1)
    pre = (rows - d) ** 2

    temp = np.sum(pre,axis=1)
    res = 2 / (np.exp(1 / (-temp ** 0.5)) + 1) - 1
    return res

# 取某个领域的用户
def GetUserByCategory(users,category):
    temp = users['category'] == category
    users = users[temp == True]
    return users

# 计算代表性矩阵
def GetRepreMatrix(users,category):
    users = GetUserByCategory(users,category)
    feature = ['friends','followers','statuses','favourites','gender','verified','city','urank']

    # 先做归一化处理
    users[feature] = (users[feature] - users[feature].min()) / (users[feature].max() - users[feature].min())
    users = users.fillna(0)
    res = repre(users,0,feature)
    i = 1
    while i < len(users.index):
        res = np.vstack((res,repre(users,i,feature)))
        i += 1
    R = np.matrix(res)
    np.save("R/%sRepresentativeMatrix.npy" % category,R)

def test():
    categories = ["Actor","Singer","Director","Player","Common"]

    # 将所用用户写入csv文件
    # users = GetAllUsersFeature()
    # WriteIntoCSV(users)

    # users = GetUsersFromCSV()

    # WriteIntoCSVByCategory('Common')

    users = GetUsersFromCSVByCategory('Actor')
    # print len(users)
    # WriteIntoCSVByCategory('Singer')
    # 得到代表性矩阵
    # GetRepreMatrix(users,"Singer")

    # 得到关系
    GetRelationships(users,'Actor')
    # GetRelationships()
    # users = GetUsersFromCSV(category)
    # CommunityDetectionByNX("Graph/all_users_ids","Graph/all_users_rels")
    # users,R,id_list,g = init.Init(category)
    # GenerateNeighbours(category,id_list,g)
    # GetRepreMatrix(users,category)
    # print users.index

    # features = GetFeatureColumns()
    # start_time = time.time()
    # print r(users.iloc[1][features],users.iloc[1][features])
    # end_time = time.time()
    # print "cost %f s" % (end_time - start_time)
# GetRepreMatrix(GetUsersFromCSV("Religion"),"%s_ids" % "Religion","%s_rels" % "Religion")
test()
