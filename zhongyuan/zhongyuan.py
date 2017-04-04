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
#导入mysql.py，连接数据库
import mysql
#导入多进程库
from multiprocessing import Pool
import gc
#解决python进程池调用类方法不执行问题
import copy_reg
import types
#import sys
#sys.setrecursionlimit(1000000)
#解决python进程池调用类方法不执行问题
def _reduce_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)
copy_reg.pickle(types.MethodType, _reduce_method)

#中原地产爬虫类
class ZYDC:

	#初始化方法，定义一些变量
	def __init__(self,baseUrl,page,headers):
		#列表页固定部分
		self.baseUrl = baseUrl
		#页面可变部分
		self.page = page
		#设置请求头部信息
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} 

	#传入某一页的索引获得该页面的房源链接
	def getPage(self,pageIndex):
		try:
			url = self.baseUrl + self.page + str(pageIndex) + '/'
			request = requests.get(url=url, headers=self.headers)
			htm = request.content
			zy = BeautifulSoup(htm, 'html.parser')
			houseurls = zy.find_all('a', attrs={'class':'cBlueB'})
			urls = []
			for x in houseurls:
				urls.append(x.get('href'))
			return urls
		except Exception as e:
			if hasattr(e, "reason"):
				print "连接中原地产失败，错误原因",e.reason
				return None

	#获取所有页面的房源链接
	def getAllUrl(self,pageIndex):
		urls = self.getPage(pageIndex)
		return urls

	#获取某一房源的具体信息
	#def getHouseInfo(self):
	#	houseurls = self.mysql.selectData('houseurl','url')

	#主函数
	def main(self,pageIndex):
		f_html = open('houseUrl.txt','w')
		#进程池，4个进程并发
		pool = Pool(processes=4)
		#for page in pageIndex:
		#	print pool.apply_async(self.getAllUrl, (pageIndex,))
		#join()将列表转为字符串
		poolurl = pool.map(self.getAllUrl, pageIndex)
		urls = []
		map(urls.extend, poolurl)
		f_html.write('\n'.join(urls))
		#关闭进程池，进程池不会再创建新的进程
		pool.close()
		#等待进程池中的全部进程执行完毕，防止主进程再worker进程结束前结束
		pool.join()
		f_html.close()
		#连接数据库
		self.mysql = mysql.Mysql()
		for i in range(0,len(urls)):
			url_dict = {"url": urls[i],}
			self.mysql.insertData('houseurl', url_dict)


	#将信息存入数据库
	def insertDb(self):
		for i in range(0,len(self.hu)):
			house_dict = {
			"house_url": self.hu[i],
			"houseinfo_xhm": self.hi1[i],
			"houseinfo_clzn": self.hi2[i],
			"houseprice": self.hp[i],
			"followinfo": self.hsi[i],
			}
			self.mysql.insertData('ZYDC', house_dict)
		
#执行函数
if __name__ == "__main__":
	start = time.clock()
	print time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
	#设置列表页固定部分
	url = 'http://sz.centanet.com/ershoufang/'
	#设置页面可变部分
	page = ('g')
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} 
	#运行爬虫类
	spider = ZYDC(url,page,headers)
	#获取第一页的所有代码
	url1 = url + page + str(1) + '/'
	request = requests.get(url=url1, headers=headers)
	html1 = request.content
	#获取房源总数量
	houseNum = int(re.findall(r".*?<span.*?cRed.*?<em>(.*?)</em>", html1)[0])
	#获取总页数
	TotalPage = houseNum/25 + 1
	#每个页面
	pages = [p for p in range(1,TotalPage+1)]
	#TotalPages = [pages[i:i+10] for i in range(0,TotalPage,10)]
	#print houseNum
	#for i in range(0,len(TotalPages)):
	#	spider = ZYDC(url,page)
	#	spider.main(TotalPages[i])
	spider = ZYDC(url,page,headers)
	spider.main(pages)
	print time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
	end = time.clock()
	print str(end-start) + 's'

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
'''
