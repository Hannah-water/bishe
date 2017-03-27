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
housedb = pd.read_sql('select * from ZYDC', con=conn)
conn.close()
#查看数据表内容
housedb.head()

#对房源信息进行分列
houseinfo1_split = pd.DataFrame((x.split('|') for x in housedb.houseinfo_xhm),index=housedb.index,columns=['xiaoqu','huxing','mianji'])
houseinfo2_split = pd.DataFrame((x.split('|') for x in housedb.houseinfo_clzn),index=housedb.index,columns=['chaoxiang','louceng','zhuangxiu','niandai'])
#查看分列结果
houseinfo1_split.head()
houseinfo2_split.head()
#将分列结果拼接起来
houseinfo = pd.merge(houseinfo1_split,houseinfo2_split,right_index=True,left_index=True)
#将分列结果拼接回原数据表
house = pd.merge(housedb,houseinfo,right_index=True,left_index=True)
#查看拼接后的数据表
house.head()


#按房源小区类别进行汇总
xiaoqu = house.groupby('xiaoqu')['xiaoqu'].agg(len)
#查看小区汇总结果
xiaoqu

#按房源户型类别进行汇总
huxing = house.groupby('huxing')['huxing'].agg(len)
#查看户型汇总结果
huxing

#按房源面积类别进行汇总
mianji = house.groupby('mianji')['mianji'].agg(len)
#查看面积汇总结果
mianji

#按房源朝向类别进行汇总
chaoxiang = house.groupby('chaoxiang')['chaoxiang'].agg(len)
#查看朝向汇总结果
chaoxiang

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


#plt.rcParams['font.sans-serif'] = ['SimHei']
#绘制房源户型分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(12,9))
#创建一个一维数组赋值给a
a=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
#创建条形图，参数为户型类别，颜色，透明度和图表边框
plt.barh([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37],huxing,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置x轴标题
plt.ylabel(u'户型')
#设置y轴标题
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