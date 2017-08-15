#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import MySQLdb
import MySQLdb.cursors
import numpy as np
import Distance
# 每个样本的格式[Followers/Following,Activity,Influence,Interests_tags,location,category]
class TwitterUser:
    def __init__(self,userid,fratio,activity,influence,interest_tags,location,category):
        self.userid = userid
        self.fratio = fratio
        self.activity = activity
        self.influence = influence
        self.interest_tags = interest_tags
        self.location = location
        self.category = category


# 数据库连接
def Connection():
    conn = MySQLdb.connect(
        host= "localhost",
        port = 3306,
        user= "root",
        passwd= "123",
        db = "TwitterUserInfo",
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

# 获取用户的特征向量
def GetUserFeature(userid,table="StandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s where userid = '%s'" % (table,userid))
    data = cursor.fetchall()
    twitter_user = TwitterUser(data[0]['userid'],data[0]['followers_count'] * 1.0 / data[0]['friends_count'],data[0]['activity'],data[0]['influenceScore'],data[0]['interest_tags'],data[0]['time_zone'],data[0]['category'])
    Close(conn,cursor)
    return twitter_user

# 获取所有用户的特征向量
def GetUsersFeature(table="StandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s" % table)
    datas = cursor.fetchall()
    users = []
    for data in datas:
        if data['friends_count'] == 0:
            fratio = data['followers_count'] * 1.0 / 1
        else:
            fratio = data['followers_count'] * 1.0 / data['friends_count']
        twitter_user = TwitterUser(data['userid'],fratio,data['activity'],data['influenceScore'],data['interest_tags'],data['time_zone'],data['category'])
        users.append(twitter_user)
    Close(conn,cursor)
    return users

# 获取用户所有的时区,用来映射location属性
def GetUserLocation(table="StandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT distinct(time_zone) FROM %s" % table)
    datas = cursor.fetchall()
    location = []
    for data in datas:
        location.append(data['time_zone'])
    Close(conn,cursor)
    return location

# 获取用户所有的类别,用来映射category属性
def GetUserCategory(table="StandardUsers"):
    conn,cursor = Connection()
    cursor.execute("SELECT distinct(category) FROM %s" % table)
    datas = cursor.fetchall()
    categories = []
    for data in datas:
        categories.append(data['category'])
    Close(conn,cursor)
    return categories

# 构造字典形式的特征向量全集
def GenerateFeatures(users,table="StandardUsers"):
    '''
    :param users: 用户全集
    '''
    features = []
    locations = GetUserLocation(table)

    categories = GetUserCategory(table)

    for user in users:
        features.append((user.fratio,user.activity,user.influence,user.interest_tags.split(","),user.location,user.category,user.userid))
    return features

# 获取原集中的领域分布
def CategoriesDistribution(table="StandardUsers"):
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
        features3.append(feature[:3])
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
        pre_feature.append(r[0])
        pre_feature.append(r[1])
        pre_feature.append(r[2])
        normal_feature = pre_feature + list(feature[3:])
        new_features.append(normal_feature)
    return new_features

# 得到最终的特征全集
def Features(table="StandardUsers"):
    features = GenerateFeatures(GetUsersFeature(table))
    new_features = Normalized(features)
    features = {}
    for feature in new_features:
        userid = feature[len(feature) - 1]
        features[userid] = feature[:-1]
    return features

def Initial(features,k):
    '''

    :param k: 随机初始化k个向量
    :return: 返回
    '''
    # 随机选择k个作为初始均值向量(使得选择的种子包含了所有的类别
    k_seeds = set()
    i = 0
    while len(k_seeds) < k:
        for key in features.keys():
            if features[key][5] == (i % k) and key not in k_seeds:
                k_seeds.add(key)
                break
        i += 1
    print "%d个种子已选好" % k
    return k_seeds

# 根据字典的value值查找key值
def find_key(dict,value):
    for key in dict.keys():
        if value == dict[key]:
            return key
    return None

# 将人物按领域分类
def People():
    features = Features()
    # 将人物按领域分类
    people = {}
    for key in features.keys():
        if features[key][5] not in people.keys():
            people[features[key][5]] = [key]
        else:
            people[features[key][5]].append(key)
    return people

# 测试距离
def test():
    table = "StandardUsers"
    dist = 0
    features = Features(table)
    for key1 in features.keys():
        for key2 in features.keys():
            dist += Distance.distance(features[key1],features[key2])
    n = len(features.keys())
    print dist / (n * (n - 1) / 2)

# test()