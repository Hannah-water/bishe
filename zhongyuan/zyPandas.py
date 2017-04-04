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

#按房源户型类别进行汇总
huxing_group = house.groupby('huxing')['huxing'].agg(len)

#按房源朝向类别进行汇总
chaoxiang_group = house.groupby('chaoxiang')['chaoxiang'].agg(len)

'''
#按房源小区类别进行汇总
xiaoqu_group = house.groupby('xiaoqu')['xiaoqu'].agg(len)
#查看小区汇总结果
xiaoqu_group

#按房源楼层类别进行汇总
louceng = house.groupby('louceng')['louceng'].agg(len)
#查看楼层汇总结果
louceng

#按房源装修类别进行汇总
zhuangxiu = house.groupby('zhuangxiu')['zhuangxiu'].agg(len)
#查看装修汇总结果
zhuangxiu

#按房源年代类别进行汇总
niandai = house.groupby('niandai')['niandai'].agg(len)
#查看年代汇总结果
niandai

#按带看数进行汇总
follow = house.groupby('followinfo')['followinfo'].agg(len)
#查看带看数汇总结果
follow
'''

'''
#plt.rcParams['font.sans-serif'] = ['SimHei']
#绘制房源户型分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(12,9))
#创建一个一维数组赋值给a
a = np.arange(1,38,1)
#a=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
#创建条形图，参数为户型类别，颜色，透明度和图表边框
plt.barh(a,huxing_group,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置y轴标题
plt.ylabel(u'户型')
#设置x轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,6000)
plt.ylim(0,37)
#设置图表标题
plt.title(u'房源户型分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称
plt.yticks(a,(u'1室0厅',u'1室1厅',u'1室2厅',u'2室0厅',u'2室1厅',u'2室2厅',u'3室0厅',u'3室1厅',u'3室2厅',u'3室3厅',u'4室0厅',u'4室1厅',u'4室2厅',u'4室3厅',u'5室1厅',u'5室2厅',u'5室3厅',u'5室4厅',u'5室5厅',u'6室0厅',u'6室2厅',u'6室3厅',u'6室4厅',u'6室5厅',u'6室6厅',u'7室2厅',u'7室3厅',u'7室4厅',u'7室6厅',u'8室2厅',u'8室3厅',u'8室4厅',u'9室2厅',u'9室3厅',u'9室4厅',u'9室6厅'))
#显示图表
plt.show()
'''
'''
#绘制房源带看数分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(8,6))
#创建一个一维数组赋值给a
a = np.arange(1,7,1)
#创建条形图，参数为带看数分组，颜色，透明度和图表边框
plt.barh(a,follow_group.drop('0'),color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置x轴标题
plt.ylabel(u'带看数分组')
#设置y轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,1000)
plt.ylim(0,7)
#设置图表标题
plt.title(u'房源带看数分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称
plt.yticks(a,('1','2-5','6-9','10-13','14-17',u'18以上'))
#显示图表
plt.show()
'''
'''
#绘制房源面积分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(8,6))
#创建一个一维数组赋值给a
a = np.arange(1,12,1)
#创建条形图，参数为面积分组，颜色，透明度和图表边框
plt.barh(a,mianji_group,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置y轴标题
plt.ylabel(u'面积分组')
#设置x轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,9000)
plt.ylim(0,12)
#设置图表标题
plt.title(u'房源面积分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称
plt.yticks(a,tuple(mianji_group_label))
#显示图表
plt.show()
'''

'''
#绘制房源朝向分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(8,6))
#创建一个一维数组赋值给a
a = np.arange(1,12,1)
#创建条形图，参数为朝向分组，颜色，透明度和图表边框
plt.barh(a,chaoxiang_group,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置y轴标题
plt.ylabel(u'朝向分组')
#设置x轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,6000)
plt.ylim(0,12)
#设置图表标题
plt.title(u'房源朝向分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称
plt.yticks(a,(u'东',u'东北',u'东南',u'东西',u'北',u'南',u'南北',u'没有注明',u'西',u'西北',u'西南'))
#显示图表
plt.show()
'''

