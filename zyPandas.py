#-*-coding:utf-8 -*-
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np
#导入mysql.py，连接
import MySQLdb

#连接数据库，创建数据表
conn = MySQLdb.connect(host='localhost',user='root',passwd='121261',db='ZYDC_DB',port=3306,charset='utf8')
house = pd.read_sql('select * from ZYDC', con=conn)
conn.close()
#查看数据表内容
house.head()

#对房源信息进行分列
houseinfo1_split = pd.DataFrame((x.split('|') for x in house.houseinfo_xhm),index=house.index,columns=['xiaoqu','huxing','mianji'])
houseinfo2_split = pd.DataFrame((x.split('|') for x in house.houseinfo_clzn),index=house.index,columns=['chaoxiang','louceng','zhuangxiu','niandai'])
#查看分列结果
houseinfo1_split.head()
houseinfo2_split.head()
#将分列结果拼接起来
houseinfo = pd.merge(houseinfo1_split,houseinfo2_split,right_index=True,left_index=True)
#将分列结果拼接回原数据表
house = pd.merge(house,houseinfo,right_index=True,left_index=True)
#查看拼接后的数据表
house.head()

'''
#创建数据表
array = {'followinfo':spider.hsi, 'houseprice':spider.hp, 'houseinfo1':spider.hi1, 'houseinfo2':spider.hi2}
house = pd.DataFrame.from_dict(array, orient='index').transpose()
#查看数据表的内容
house.head()

#对房源信息进行分列
houseinfo1_split = pd.DataFrame((x.split('|') for x in house.houseinfo1),index=house.index,columns=['xiaoqu','huxing','mianji'])
houseinfo2_split = pd.DataFrame((x.split('|') for x in house.houseinfo2),index=house.index,columns=['chaoxiang','louceng','zhuangxiu','niandai'])
#查看分列结果
houseinfo1_split.head()
houseinfo2_split.head()
#将分列结果拼接起来
houseinfo = pd.merge(houseinfo1_split,houseinfo2_split,right_index=True,left_index=True)
#将分列结果拼接回原数据表
house = pd.merge(house,houseinfo,right_index=True,left_index=True)
#查看拼接后的数据表
house.head()

#按房源户型类别进行汇总
huxing = house.groupby('huxing')['huxing'].agg(len)
#查看户型汇总结果
huxing
'''