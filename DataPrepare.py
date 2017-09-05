#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import MySQLdb.cursors
import numpy as np
import random
import csv

# 每个样本的格式[Followers/Following,Activity,Influence,Interests_tags,location,category]
class TwitterUser:
    def __init__(self,userid,followers,activity,influence,friends,location,category,interest_tags):
        self.userid = userid
        self.followers = followers
        self.activity = activity
        self.influence = influence
        self.interest_tags = interest_tags
        self.location = location
        self.category = category
        self.friends = friends

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

# 获取所有用户的id
def GetUsersId(table="newStandardUsers"):
    # 结果以集合的方式返回
    conn,cursor = Connection()
    ids = set()
    cursor.execute("SELECT * FROM %s" % table)
    datas = cursor.fetchall()
    for data in datas:
        ids.add(data['user_id'])
    Close(conn,cursor)
    return ids

# 获取用户的特征向量
def GetUserFeature(userid,table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s where userid = '%s'" % (table,userid))
    data = cursor.fetchall()
    twitter_user = TwitterUser(data[0]['user_id'],data[0]['followers_count'] * 1.0,data[0]['activity'],data[0]['influence_score'], data[0]['friends_count'] * 1.0,data[0]['time_zone'],data[0]['category'],data[0]['interest_tags'])
    Close(conn,cursor)
    return twitter_user

# 获取所有用户的特征向量
def GetUsersFeature(table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s" % table)
    datas = cursor.fetchall()
    users = []
    for data in datas:
        twitter_user = TwitterUser(data['user_id'],float(data['followers_count']),data['activity'],data['influence_score'],float(data['friends_count']),data['time_zone'],data['category'],data['interest_tags'] )
        users.append(twitter_user)
    Close(conn,cursor)
    return users

# 获取用户所有的时区,用来映射location属性
def GetUserLocation(table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT distinct(time_zone) FROM %s" % table)
    datas = cursor.fetchall()
    location = []
    for data in datas:
        location.append(data['time_zone'])
    Close(conn,cursor)
    return location

# 获取用户所有的类别,用来映射category属性
def GetUserCategory(table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT distinct(category) FROM %s" % table)
    datas = cursor.fetchall()
    categories = []
    for data in datas:
        categories.append(data['category'])
    Close(conn,cursor)
    return categories

# 构造字典形式的特征向量全集
def GenerateFeatures(users):
    '''
    :param users: 用户全集
    '''
    features = []

    for user in users:
        features.append((user.followers,user.activity,user.influence,user.friends,user.location,user.category,user.interest_tags.split(","),user.userid))
    return features

# 获取原集中的领域分布
def CategoriesDistribution(table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT category,count(*) as number from %s group by category" % table)
    datas = cursor.fetchall()
    categories = {}
    for data in datas:
        categories[data['category']] = data['number']
    cursor.execute("SELECT count(*) as number FROM %s" % table)
    datas = cursor.fetchall()
    for data in datas:
        total_number = data['number']
    Close(conn,cursor)
    for category in categories.keys():
        categories[category] = categories[category] * 1.0 / total_number
    return categories

# 前三个特征需要归一化:采用z-score标准化
def Normalized(features):
    features3 = []
    for feature in features:
        features3.append(feature[:4])
    x = np.array(features3).astype(float)
    # 以列来计算
    xr = np.rollaxis(x,axis=0)
    # 计算平均值
    xr -= np.mean(x,axis=0)
    # 计算标准差
    xr /= np.std(x,axis=0)
    new_features = []
    for r,feature in zip(xr,features):
        pre_feature = []
        # r[0]是followers
        pre_feature.append(r[0] / 100)
        pre_feature.append(r[1])
        pre_feature.append(r[2])
        pre_feature.append(r[3] / 100)
        normal_feature = pre_feature + list(feature[4:])
        new_features.append(normal_feature)
    return new_features

# 得到最终的特征全集
def Features(table="newStandardUsers"):
    features = GenerateFeatures(GetUsersFeature(table))
    # 归一化完成
    features = Normalized(features)
    print "归一化完成"
    new_features = {}
    for feature in features:
        userid = feature[len(feature) - 1]
        new_features[userid] = feature
    return new_features

def Initial(features,k):
    '''

    :param k: 随机初始化k个向量
    :return: 返回
    '''
    ids = features.keys()
    number = len(ids)
    # 随机选择k个作为初始向量
    k_seeds = set()
    while len(k_seeds) < k:
        id = random.randint(0,number - 1)
        key = ids[id]
        if key not in k_seeds:
            k_seeds.add(key)
    print "%d个种子已选好" % k
    return k_seeds

# 根据字典的value值查找key值
def find_key(dict,value):
    for key in dict.keys():
        if value == dict[key]:
            return key
    return None

# 返回某个领域的用户id
def GetPeopleIdByDomain(domain,table="newStandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT user_id FROM %s where category = '%s'" % (table,domain))
    datas = cursor.fetchall()
    tuples = []
    for data in datas:
        tuples.append(data['user_id'])
    Close(conn,cursor)
    return tuples

# 将人物按领域分类
def People(features):
    people = {}
    for feature in features.keys():
        if features[feature][5] not in people.keys():
            people[features[feature][5]] = [feature]
        else:
            people[features[feature][5]].append(feature)
    return people

# 根据id构建字典
def FeaturesById(profiles,features):
    people = {}
    for profile in profiles:
        people[profile] = features[profile]
    return people

# 统计profiles集合中每个领域相应的人数
def DomainDistribution(profiles,features):
    categories = {}
    for profile in profiles:
        if features[profile][5] not in categories.keys():
            categories[features[profile][5]] = 1
        else:
            categories[features[profile][5]] += 1
    return categories

# 为存入neo4j做准备

def Write2CSV(users,path):
    # 将所有的用户作为节点,存入CSV文件中
    with open(path,'wb') as csvfile:
        count = 0
        writer = csv.writer(csvfile)
        # 写入CSV文件的标题
        writer.writerow(['userid:ID','fratio','activity','influence','interest_tags','location','category',":LABEL"])
        twitter_users = []
        for user in users:
            temp = (user.userid,user.fratio,user.activity,user.influence,user.interest_tags,user.location,user.category,"TwitterUser")
            twitter_users.append(temp)
            count += 1
        writer.writerows(twitter_users)
        csvfile.close()
        print "共计写入%d个用户" % count

# 测试距离
def test():
    Write2CSV(GetUsersFeature(),"/home/duncan/104071Users.csv")

# test()