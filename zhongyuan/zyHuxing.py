#-*-coding:utf-8 -*-
#导入zyPandas.py
import zyPandas
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np

#plt.rcParams['font.sans-serif'] = ['SimHei']
#绘制房源户型分布条形图
#设置条形图的字体大小
plt.rc('font', family='SimHei', size=12)
#设置条形图的尺寸
plt.figure(figsize=(12,9))
#创建一个一维数组赋值给a
a = np.arange(1,41,1) #38
#a=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37])
#创建条形图，参数为户型类别，颜色，透明度和图表边框
plt.barh(a,zyPandas.huxing_group,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
#设置y轴标题
plt.ylabel(u'户型')
#设置x轴标题
plt.xlabel(u'数量')
#设置坐标轴的刻度
plt.xlim(0,7000)
plt.ylim(0,41) #37
#设置图表标题
plt.title(u'房源户型分布情况')
#设置图例，并设置在图表中的显示位置
plt.legend([u'数量'], loc='upper right')
#设置背景网格线的颜色，样式，尺寸和透明度
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
#设置y轴数据分类名称 36
plt.yticks(a,(u'1室0厅',u'1室1厅',u'1室2厅',u'2室0厅',u'2室1厅',u'2室2厅',u'2室3厅',u'3室0厅',u'3室1厅',u'3室2厅',u'3室3厅',u'4室0厅',u'4室1厅',u'4室2厅',u'4室3厅',u'4室4厅',u'5室1厅',u'5室2厅',u'5室3厅',u'5室4厅',u'5室5厅',u'6室1厅',u'6室2厅',u'6室3厅',u'6室4厅',u'6室5厅',u'6室6厅',u'7室1厅',u'7室2厅',u'7室3厅',u'7室4厅',u'7室6厅',u'8室2厅',u'8室3厅',u'8室4厅',u'8室5厅',u'9室2厅',u'9室3厅',u'9室4厅',u'9室6厅'))
#保存图表
plt.savefig('zyImage/huxing.png')
#显示图表
plt.show()