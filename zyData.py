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

#连接数据库
mysql = mysql.Mysql()

#获取某一房源的具体信息
def getHouseInfo(houseUrl):
	try:
		url = 'http://sz.centanet.com' + str(houseUrl)
		#print url
		headers = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		}
		#s = requests.session()
	  	#s.keep_alive = False
		#requests.adapters.DEFAULT_RETRIES = 5
		request = requests.get(url=url, headers=headers)
		house_html = request.content
		zy_fang = BeautifulSoup(house_html, 'html.parser')
		#获取房源带看数
		followInfo = zy_fang.find_all('li', attrs={'class':'second f999'})
		follow = ''
		if len(followInfo):
			follow = followInfo[-1].get_text().replace('\n','')
		#获取房源价格/户型/面积等信息
		house1 = zy_fang.find_all('div', attrs={'class': 'roombase-price'})[0].contents
		houseinfo1 = ''
		if house1[-1].string == '\n':
			house1.pop()
		if len(house1):
			for x in house1:
				if x.string == None:
					continue
				if x.string == '\n':
					continue
				if x.string == house1[-1].string:
					houseinfo1 += x.string.replace('\n','')
				else:
					houseinfo1 += x.string.replace('\n','') + '|'
		#获取房源朝向/年代/楼层/装修/小区名称/小区地址等信息
		house2 = zy_fang.find_all('div', attrs={'class': 'txt_r f666'})
		houseinfo2 = ''
		if len(house2):
			for y in house2:
				if y.string == None:
					y.string = ''
				if y.string == house2[-1].string:
					houseinfo2 += y.string.strip().replace('\r\n','')
				else:
					houseinfo2 += y.string.strip() + '|'
		#将获取的数据存入数据库
		house_dict = {
		"house_url": url,
		"follow": follow,
		"price_area": houseinfo1,
		"houseinfo": houseinfo2,
		}
		mysql.insertData('zydc', house_dict)
	except Exception as e:
		if hasattr(e, "reason"):
			print "获取数据失败，错误原因",e.reason
			return None

#获取所有房源链接
def getHouseUrl(houseUrl):
	return houseUrl

#主函数
def main():
	houseurls = []
	#从数据库中获取所有房源url
	map(houseurls.extend, mysql.selectData('houseurl','url'))
	#进程池，4个进程并发
	pool = Pool(processes=4)
	#获取房源所有链接
	poolurl = pool.map(getHouseUrl, houseurls)
	#去除列表重复元素
	poolurl = list(set(poolurl))
	#获取链接所指向的房源具体信息
	#for i in range(0,len(poolurl),500):
	#	pool.map(getHouseInfo, poolurl[i:i+500])
	#	time.sleep(5)
	pool.map(getHouseInfo, poolurl)
	#关闭进程池，进程池不会再创建新的进程
	pool.close()
	#等待进程池中的全部进程执行完毕，防止主进程再worker进程结束前结束
	pool.join()



#执行函数
if __name__ == "__main__":
	start = time.time()
	print time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
	#运行获取房源信息的爬虫
	main()
	end = time.time()
	print time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
	print str(end-start) + 's'
