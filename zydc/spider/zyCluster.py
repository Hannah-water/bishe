#-*-coding:utf-8 -*-
#导入zyPandas.py
import zyPandas
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np
#导入sklearn中的KMeans进行聚类分析
from sklearn.cluster import KMeans

#聚类分析

#使用房源总价，面积和带看数三个字段进行聚类
house_type = np.array(zyPandas.house[['houseprice_num','mianji_num','follow_num']])
#设置质心数量为3
clf = KMeans(n_clusters=3)
#计算聚类结果
clf = clf.fit(house_type)
#查看分类结果的中心坐标
clf.cluster_centers_

#在原数据表中标注所属类别
zyPandas.house['label'] = clf.labels_

#提取不同类别的数据
house0 = zyPandas.house.loc[zyPandas.house['label'] == 0]	#总价低，面积低，带看数高
house1 = zyPandas.house.loc[zyPandas.house['label'] == 1]	#总价高，面积高，带看书低
house2 = zyPandas.house.loc[zyPandas.house['label'] == 2]	#总价中，面积中，带看数中

#绘制房源总价与面积聚类结果的散点图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(12,9))
#创建散点图
plt.scatter(house0['houseprice_num'], house0['mianji_num'],color='#99CC01',marker='+',linewidth=2,alpha=0.8)	#绿
plt.scatter(house1['houseprice_num'], house1['mianji_num'],color='#FE0000',marker='+',linewidth=2,alpha=0.8)	#红
plt.scatter(house2['houseprice_num'], house2['mianji_num'],color='#0000FE',marker='+',linewidth=2,alpha=0.8)	#蓝
#设置x轴标题
plt.xlabel(u'房源总价（万元）')
#设置y轴标题
plt.ylabel(u'房源面积（平米）')
#设置坐标轴的刻度
plt.xlim(0,20000)
#设置图表标题
plt.title(u'房价-面积-带看数聚类分析')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#保存图表
plt.savefig('zyImage/cluster.png')
plt.savefig('zydc/static/images/cluster.png')
#显示图表
plt.show()