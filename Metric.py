#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

import Distance as dist

a = 2
b = 2
#　子集的代表性衡量
def metric(origin_features,profile_features):
    size_profile = len(profile_features.keys())
    total_number = len(origin_features.keys())
    part1 = 0
    for origin in origin_features.keys():
        min = dist.distance(origin_features[origin],profile_features[profile_features.keys()[0]])
        # 在profile中选取到该对象距离最小的值
        for profile in profile_features:
            if dist.distance(origin_features[origin],origin_features[profile]) < min:
                min = dist.distance(origin_features[origin],origin_features[profile])
        part1 += min

    # 第二部分由与profile大小相关的惩罚值函数构成
    part2 = b * size_profile * 1.0 / total_number
    loss = part1 + part2
    return loss