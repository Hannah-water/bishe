#-*-coding:utf-8 -*-
#导入zyPandas.py
import zyPandas
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np

#绘制房源朝向分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(12,9))
#创建一个一维数组赋值给a
a = np.arange(1,13,1)
#创建条形图，参数为朝向分组，颜色，透明度和图表边框
plt.barh(a,zyPandas.chaoxiang_group,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置y轴标题
plt.ylabel(u'朝向分组')
#设置x轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,7000)
plt.ylim(0,13)
#设置图表标题
plt.title(u'房源朝向分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称
plt.yticks(a,(u'不限',u'东',u'东北',u'东南',u'东西',u'北',u'南',u'南北',u'没有注明',u'西',u'西北',u'西南'))
#保存图表
plt.savefig('zyImage/chaoxiang.png')
#显示图表
plt.show()