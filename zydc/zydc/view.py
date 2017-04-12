#-*-coding:utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf

def index(request):
	context = {}
	if request.POST.has_key("getUrl"):
		#execfile('spider/zhongyuan.py')
		from spider import zhongyuan
		context['state'] = '成功获取全部房源链接'
		context['houseUrl'] = open('spider/houseUrl.txt').read()
		context['disabled1'] = 'disabled="disabled"'
	elif request.POST.has_key("getInfo"):
		#execfile('spider/zyData.py')
		from spider import zyData
		context['houseInfo'] = '成功获取全部房源信息'
		context['disabled2'] = 'disabled="disabled"'
	elif request.POST.has_key("dataAnalysis"):
		from spider import zyHuxing
		from spider import zyMianji
		from spider import zyFollow
		from spider import zyDistrict
		from spider import zyChaoxiang
		from spider import zyYear
		from spider import zyCluster
		#execfile('spider/zyHuxing.py')
		#execfile('spider/zyMianji.py')
		#execfile('spider/zyFollow.py')
		#execfile('spider/zyDistrict.py')
		#execfile('spider/zyChaoxiang.py')
		#execfile('spider/zyYear.py')
		#execfile('spider/zyCluster.py')
		context['state'] = '成功进行数据分析'
		context['huxing'] = zyHuxing.zyPandas.huxing_group
		context['mianji'] = zyHuxing.zyPandas.mianji_group
		context['diqu'] = zyHuxing.zyPandas.district_group
		context['daikan'] = zyHuxing.zyPandas.follow_group
		context['chaoxiang'] = zyHuxing.zyPandas.chaoxiang_group
		context['niandai'] = zyHuxing.zyPandas.niandai_group
		context['disabled3'] = 'disabled="disabled"'
	elif request.POST.has_key("cluster_center"):
		from spider import zyCluster
		context['state'] = '房价-面积-带看数'
		context['center'] = zyCluster.clf.cluster_centers_
	elif request.POST.has_key("data"):
		from spider import zyPandas
		context['data'] = open('spider/house.csv').read()
		return render(request, 'data.html', context)
	return render(request, 'index.html', context)


def huxing(request):
	context = {}
	context['huxing'] = '/static/images/huxing.png'
	return render(request, 'huxing.html', context)

def mianji(request):
	context = {}
	context['mianji'] = '/static/images/mianji.png'
	return render(request, 'mianji.html', context)

def diqu(request):
	context = {}
	context['diqu'] = '/static/images/district.png'
	return render(request, 'diqu.html', context)

def daikan(request):
	context = {}
	context['daikan'] = '/static/images/follow.png'
	return render(request, 'daikan.html', context)

def chaoxiang(request):
	context = {}
	context['chaoxiang'] = '/static/images/chaoxiang.png'
	return render(request, 'chaoxiang.html', context)

def niandai(request):
	context = {}
	context['niandai'] = '/static/images/year.png'
	return render(request, 'niandai.html', context)

def cluster(request):
	context = {}
	context['cluster'] = '/static/images/cluster.png'
	context['cluster_plus'] = '/static/images/cluster_plus.png'
	return render(request, 'cluster.html', context)