#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import MySQLdb.cursors
import csv
import FastNewman as cnm
import TwitterWithNeo4j as neo4j
import cPickle as pickle
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community.asyn_lpa import asyn_lpa_communities
from networkx.algorithms.community.asyn_fluidc import asyn_fluidc
from networkx.algorithms.community.quality import coverage
from networkx.algorithms.community.quality import performance
from networkx.algorithms.community.community_utils import is_partition

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


# 数据库连接
def Connection():
    conn = MySQLdb.connect(
        host= "192.168.131.191",
        port = 3306,
        user= "duncan",
        passwd= "123",
        db = "twitter_users",
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
def GetAllUsersFeature(table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s" % table)
    datas = cursor.fetchall()
    users = []
    for data in datas:
        twitter_user = Twitter_User(data['user_id'],int(data['followers_count']),int(data['friends_count']),int(data['statuses_count']),int(data['favourites_count']),float(data['activity']),float(data['influence_score']),data['time_zone'],data['protected'],data['verified'],data['category'])
        # users.append(twitter_user)
        users.append((data['user_id'],int(data['followers_count']),int(data['friends_count']),int(data['statuses_count']),int(data['favourites_count']),float(data['activity']),float(data['influence_score']),data['time_zone'],data['protected'],data['verified'],data['category']))
    Close(conn,cursor)
    return users

# 获取某个领域的所有用户的特征向量
def GetUsersFeature(category,table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s where category = '%s'" % (table,category))
    datas = cursor.fetchall()
    users = []
    for data in datas:
        # twitter_user = Twitter_User(data['user_id'],int(data['followers_count']),int(data['friends_count']),int(data['statuses_count']),int(data['favourites_count']),float(data['activity']),float(data['influence_score']),data['time_zone'],data['protected'],data['verified'],data['category'])
        # users.append(twitter_user)
        users.append((data['user_id'],int(data['followers_count']),int(data['friends_count']),int(data['statuses_count']),int(data['favourites_count']),float(data['activity']),float(data['influence_score']),data['time_zone'],data['protected'],data['verified'],data['category']))
    Close(conn,cursor)
    return users

# 所有用户的信息label encoding后写入csv文件中
def WriteIntoCSV(users):
    with open("/home/duncan/TotalUsers.csv","wb") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['userid','followers','friends','statuses','favourites','activity','influence','location','protected','verified','category'])
        writer.writerows(users)

def GetRelationships(catgegory):
    driver,session = neo4j.Conn()
    users = GetUsersFeature(catgegory)
    id_list = [user[0] for user in users]
    relationships = []
    for i in xrange(len(id_list)):
        followings = set(neo4j.GetFollowings(driver,session,id_list[i]))
        j = i + 1
        while j < len(id_list):
            if id_list[j] in followings:
                relationships.append([i,j])
            j += 1
    rel_file = open("%s_rels" % catgegory,'wb')
    ids_file = open("%s_ids" % catgegory,'wb')
    pickle.dump(relationships,rel_file,True)
    pickle.dump(id_list,ids_file,True)
    print len(relationships)

# 社区发现
def CommunityDetection(id_list_path,rels_path):
    rel_file = open(rels_path,'rb')
    rels = pickle.load(rel_file)
    ids_file = open(id_list_path,'rb')
    id_list = pickle.load(ids_file)
    # 社区发现
    print "community detection"
    cnm.fast_newman(id_list,rels,len(id_list),int(len(id_list) * 0.75))

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
    print sorted(map(sorted, next(community)))

categories = ["Politics","Sports","Military","Entertainment","Agriculture","Technology","Economy"]
for category in categories:
    GetRelationships(category)
# CommunityDetection("%s_ids" % category,"%s_rels" % category)
# CommunityDetectionByNX("%s_ids" % category,"%s_rels" % category)
