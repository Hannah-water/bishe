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
	def __init__(self,baseUrl,page):
		#列表页固定部分
		self.baseUrl = baseUrl
		#页面可变部分
		self.page = page
		#从第一页开始
		#self.pageIndex = 1
		#存放所有页面内容
		#self.html = ""
		#所有页面的内容,BeautifulSoup对象
		self.zy = BeautifulSoup('', 'html.parser')
		#存放房源链接
		self.hu = []
		#存放房源价格
		self.hp = []
		#存放房源信息
		#小区名，户型，面积
		self.hi1 = []
		#朝向，楼层，装修，年代
		self.hi2 = []
		#存放每一个房源具体信息,带看数
		self.hsi = []
		#设置请求头部信息
		self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'} 

	#传入某一页的索引获得页面内容
	def getPage(self,pageIndex):
		try:
			url = self.baseUrl + self.page + str(pageIndex) + '/'
			request = requests.get(url=url, headers=self.headers)
			htm = request.content
			return htm
		except Exception as e:
			if hasattr(e, "reason"):
				print "连接中原地产失败，错误原因",e.reason
				return None

	#获取所有页面的内容
	def getAllPage(self,pageIndex):
		html = self.getPage(pageIndex)
		return html

	#解析抓取的页面内容
	#def parserPage(self):
	#	self.zy = BeautifulSoup(self.html, 'html.parser')

	#获取房源价格
	def getPrice(self):
		housePrice = self.zy.find_all('p', attrs={'class':'price-nub cRed'})
		for x in housePrice:
			price = x.get_text()
			self.hp.append(price)

	#获取房源信息
	def getInfo(self):
		houseInfo1 = self.zy.find_all('p', attrs={'class':'f14 f000 mb_10'})
		houseInfo2 = self.zy.find_all('p', attrs={'class':'f7b mb_10'})
		for y in houseInfo1:
			house1 = y.a.string + '|' + y.span.string + '|' + y.span.next_sibling.string
			self.hi1.append(house1)
		for y in houseInfo2:
			house2 = y.get_text().replace('\r\n','').strip()
			self.hi2.append(house2)

	#获取每一个房源具体信息
	def getSpecificInfo(self):
		#获取每一个房源具体信息链接
		houseHref = self.zy.find_all('a', attrs={'class':'cBlueB'})
		#print houseHref
		#获取每一个房源具体信息
		for z in houseHref:
			house_url = 'http://sz.centanet.com' + z.get('href')
			self.hu.append(house_url)
			request = requests.get(url=house_url, headers=self.headers)
			house_html = request.content
			zy_fang = BeautifulSoup(house_html, 'html.parser')
			#获取每一个房源带看数
			followInfo = zy_fang.find_all('ul', attrs={'class':'rDetail fr'})
			for x in followInfo:
				#follow = x.li.get_text().replace('\n','') + '/' + x.li.find_next_sibling().get_text().replace('\n','')
				follow = x.li.find_next_sibling().get_text().replace('\n','')
				self.hsi.append(follow)

	#主函数
	def main(self,pageIndex):
		#print pageIndex
		f_html = open('houseHtml.txt','w')
		#进程池，4个进程并发
		pool = Pool(processes=4)
		#for page in pageIndex:
		#	print pool.apply_async(self.getAllPage, (pageIndex,))
		#join()将列表转为字符串
		#poolhtml = pool.map(self.getAllPage, pageIndex)
		#print len(poolhtml)
		f_html.write(''.join(pool.map(self.getAllPage, pageIndex)))
		#关闭进程池，进程池不会再创建新的进程
		pool.close()
		#等待进程池中的全部进程执行完毕，防止主进程再worker进程结束前结束
		pool.join()
		f_html.close()
		#f_soup = open('houseSoup.txt','w')
		self.zy = BeautifulSoup(open('houseHtml.txt'), 'html.parser')
		print self.zy
		#time.sleep(1)
		#f_soup.close()
		#self.parserPage()
		self.getPrice()
		self.getInfo()
		self.getSpecificInfo()
		self.zy = BeautifulSoup('', 'html.parser')
		#连接数据库
		self.mysql = mysql.Mysql()
		self.insertDb()
		#print self.mysql.getCurrentTime()

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
	#设置列表页固定部分
	url = 'http://sz.centanet.com/ershoufang/'
	#设置页面可变部分
	page = ('g')
	#运行爬虫类
	spider = ZYDC(url,page)
	#获取第一页的所有代码
	html1 = spider.getPage(1)
	#获取房源总数量
	houseNum = int(re.findall(r".*?<span.*?cRed.*?<em>(.*?)</em>", html1)[0])
	#获取总页数
	TotalPage = houseNum/25 + 1
	#每个页面
	pages = [page for page in range(1,TotalPage+1)]
	TotalPages = [pages[i:i+10] for i in range(0,20,10)]
	#TotalPages = [pages[i:i+10] for i in range(0,20,10)]
	for i in range(0,2):
		spider.main(TotalPages[i])
		print TotalPages[i]
	#spider.main(TotalPages[1])
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
