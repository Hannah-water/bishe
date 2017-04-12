#-*-coding:utf-8 -*-
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np
#导入mysql.py，连接
import MySQLdb
#导入sklearn中的KMeans进行聚类分析
from sklearn.cluster import KMeans

#连接数据库，创建数据表
conn = MySQLdb.connect(host='localhost',user='root',passwd='121261',db='zy_db',port=3306,charset='utf8')
housedb = pd.read_sql('select * from zydc', con=conn)
conn.close()
#查看数据表内容
housedb.head()

#对房源信息进行分列
houseinfo1_split = pd.DataFrame((x.split('|') for x in housedb.price_area),index=housedb.index,columns=['price','huxing','mianji'])
houseinfo2_split = pd.DataFrame((x.split('|') for x in housedb.houseinfo),index=housedb.index,columns=['chaoxiang','niandai','louceng','zhuangxiu','xiaoqu','address'])
#查看分列结果
houseinfo1_split.head()
houseinfo2_split.head()
#将分列结果拼接起来
houseinfo = pd.merge(houseinfo1_split,houseinfo2_split,right_index=True,left_index=True)
#将分列结果拼接回原数据表
house = pd.merge(housedb,houseinfo,right_index=True,left_index=True)
#查看拼接后的数据表
house.head()

#对房源价格进行分列
houseprice_split = pd.DataFrame((x.strip().split(u'万')[0] for x in house.price),index=house.index,columns=['houseprice_num'])
#讲分列后的房源价格拼接回数据表
house = pd.merge(house,houseprice_split,right_index=True,left_index=True)
#将houseprice_num的值都转为数字
for x in house.houseprice_num:
	index = list(house['houseprice_num']).index(x)
	if u'亿' in x:
	 	x = float(x.split(u'亿')[0]) * 10000
	house.houseprice_num[index] = x
#将hosueprice_num字段格式改为float
house['houseprice_num'] = house['houseprice_num'].astype(float)

#对带看数进行分列
fnum = []
for x in house.follow:
    if x == '':
    	x = 0
    else:
        x = x.split(u'带看')[1].strip().split(u'次')[0]
    fnum.append(x)
followinfo_split = pd.DataFrame(fnum,index=house.index,columns=['follow_num'])
#讲分列后的带看数拼接回数据表
house = pd.merge(house,followinfo_split,right_index=True,left_index=True)
#将follow_num字段格式改为float
house['follow_num'] = house['follow_num'].astype(float)
#对房源面积进行分组
#fbins = [0] + range(1,30,4)
fbins = [-1,0] + range(1,18,4) + [30]
#follow_group_label = [u'1','2-5','6-9','10-13','14-17','18-21','22-25',u'26以上']
follow_group_label = ['0','1','2-5','6-9','10-13','14-17',u'18以上']
house['follow_group'] = pd.cut(house['follow_num'], fbins, labels=follow_group_label)
#按带看数进行汇总 
follow_group = house.groupby('follow_group')['follow_group'].agg(len)
#follow_group = house.groupby('follow_num')['follow_num'].agg(len)

#对房源面积进行分列
mianji_split = pd.DataFrame((x.split(u'平')[0] for x in house.mianji),index=house.index,columns=['mianji_num'])
#讲分列后的房源面积拼接回数据表
house = pd.merge(house,mianji_split,right_index=True,left_index=True)
#将mianji_num字段格式改为float
house['mianji_num'] = house['mianji_num'].astype(float)
#查看所有房源面积范围
house['mianji_num'].min(),house['mianji_num'].max()
#对房源面积进行分组
mbins = range(0,501,50) + [900]
#mianji_group = [u'小于50','50-100','100-150','150-200','200-250','250-300','300-350','350-400','400-450','450-500','500-550','550-600','600-650','650-700','700-750','750-800','800-850','850-900']
mianji_group_label = [u'小于50','50-100','100-150','150-200','200-250','250-300','300-350','350-400','400-450','450-500',u'500以上']
house['mianji_group'] = pd.cut(house['mianji_num'], mbins, labels=mianji_group_label)
mianji_group = house.groupby('mianji_group')['mianji_group'].agg(len)

#对房源地区进行分列
area = []
for x in house.address:
    if u'【' in x:
        x = x.split(u'【')[1].strip().split(u'】')[0]
        if '/' in x:
            x = x.split('/')[0]
    else:
        x = u'没有注明'
    area.append(x)
address_split = pd.DataFrame(area,index=house.index,columns=['district'])
#讲分列后的房源地区拼接回数据表
house = pd.merge(house,address_split,right_index=True,left_index=True)
#按房源地区类别进行汇总
district_group = house.groupby('district')['district'].agg(len)

#按房源户型类别进行汇总
huxing_group = house.groupby('huxing')['huxing'].agg(len)

#按房源朝向类别进行汇总
chaoxiang_group = house.groupby('chaoxiang')['chaoxiang'].agg(len)

#对房源楼层进行分列
louceng_split = pd.DataFrame((x.split('(')[0] for x in house.louceng),index=house.index,columns=['louceng_pos'])
#讲分列后的房源楼层拼接回数据表
house = pd.merge(house,louceng_split,right_index=True,left_index=True)
#按房源楼层类别进行汇总
louceng_group = house.groupby('louceng_pos')['louceng_pos'].agg(len)

#按房源装修类别进行汇总
zhuangxiu_group = house.groupby('zhuangxiu')['zhuangxiu'].agg(len)

#对房源年代进行分列
niandai_split = pd.DataFrame((x.split(u'年')[0] for x in house.niandai),index=house.index,columns=['niandai_num'])
#讲分列后的房源年代拼接回数据表
house = pd.merge(house,niandai_split,right_index=True,left_index=True)
#将mianji_num字段格式改为float
house['niandai_num'] = house['niandai_num'].astype(int)
#按房源年代类别进行汇总
niandai_group = house.groupby('niandai_num')['niandai_num'].agg(len)

house.to_csv('spider/house.csv',encoding='utf8')
'''
#按房源小区类别进行汇总
xiaoqu_group = house.groupby('xiaoqu')['xiaoqu'].agg(len)
#查看小区汇总结果
xiaoqu_group
'''
