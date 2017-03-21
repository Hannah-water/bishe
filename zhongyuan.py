#-*-coding:utf-8 -*-
import requests
import time
import re
from bs4 import BeautifulSoup
#导入pandas库
import pandas as pd
#导入图表库
import matplotlib.pyplot as plt
#导入数值计算库
import numpy as np

#设置列表页固定部分
url = 'http://sz.centanet.com/ershoufang/'
#设置页面可变部分
page = ('g')
#设置请求头部信息
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}

for i in range(1,10):
	if i == 1:
		i = str(i)
		a = (url + page + i +'/')
		r = requests.get(url=a, headers=headers)
		html = r.content
	else:
		i = str(i)
		a = (url + page + i + '/')
		r = requests.get(url=a, headers=headers)
		html2 = r.content
		html = html + html2

#解析抓取的页面内容
zy = BeautifulSoup(html, 'html.parser')

#获取房源价格
housePrice = zy.find_all('p', attrs={'class':'price-nub cRed'})
hp = []
for x in housePrice:
	price = x.get_text()
	hp.append(price)

#获取房源信息
houseInfo = zy.find_all('p', attrs={'class':'f14 f000 mb_10'})
houseInfo2 = zy.find_all('p', attrs={'class':'f7b mb_10'})
hi = []
hi2 = []
for y in houseInfo:
	house = y.a.string + '|' + y.span.string + '|' + y.span.next_sibling.string
	hi.append(house)
for y in houseInfo2:
	house2 = y.get_text().replace('\r\n','').strip()
	hi2.append(house2)

#获取每一个房源具体信息链接
houseHref = zy.find_all('a', attrs={'class':'cBlueB'})
hh = []
#获取每一个房源具体信息
for z in houseHref:
	next_url = 'http://sz.centanet.com' + z.get('href')
	r2 = requests.get(url=next_url, headers=headers)
	next_html = r2.content
	zy_fang = BeautifulSoup(next_html, 'html.parser')
	#获取每一个房源关注度
	followInfo = zy_fang.find_all('ul', attrs={'class':'rDetail fr'})
	for x in followInfo:
		follow = x.li.get_text().replace('\n','') + '/' + x.li.find_next_sibling().get_text().replace('\n','')
		hh.append(follow)


#创建数据表
array = {'followinfo':hh, 'houseprice':hp, 'houseinfo':hi, 'houseinfo2':hi2}
house = pd.DataFrame.from_dict(array, orient='index').transpose()
#查看数据表的内容
house.head()

#对房源信息进行分列
houseinfo_split = pd.DataFrame((x.split('|') for x in house.houseinfo),index=house.index,columns=['xiaoqu','huxing','mianji'])
houseinfo2_split = pd.DataFrame((x.split('|') for x in house.houseinfo2),index=house.index,columns=['chaoxiang','louceng','zhuangxiu','niandai'])
#查看分列结果
houseinfo_split.head()
houseinfo2_split.head()
#将分列结果拼接起来
houseinfo = pd.merge(houseinfo_split,houseinfo2_split,right_index=True,left_index=True)
#将分列结果拼接回原数据表
house = pd.merge(house,houseinfo,right_index=True,left_index=True)
#查看拼接后的数据表
house.head()

#按房源户型类别进行汇总
huxing = house.groupby('huxing')['huxing'].agg(len)
#查看户型汇总结果
huxing

#按房源户型类别进行汇总
chaoxiang = house.groupby('chaoxiang')['chaoxiang'].agg(len)
#查看户型汇总结果
chaoxiang

#按房源户型类别进行汇总
xiaoqu = house.groupby('xiaoqu')['xiaoqu'].agg(len)
#查看户型汇总结果
xiaoqu

#按房源户型类别进行汇总
zhuangxiu = house.groupby('zhuangxiu')['zhuangxiu'].agg(len)
#查看户型汇总结果
zhuangxiu

#绘制房源户型分布条形图
plt.rc('font', family='STXihei', size=11)
a = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
plt.barh([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], huxing, color='#052B6C', alpha=0.8, align='center', edgecolor='white')
plt.ylabel('户型')
plt.xlabel('数量')
