#-*-coding:utf-8 -*-

from django.shortcuts import render
from django.views.decorators import csrf
#from spider import zyHuxing

def index(request):
	context = {}
	if request.POST:
		#execfile('spider/zyHuxing.py')
		from spider import zyPandas
		context['housepd'] = open('spider/house.csv').read()
	else:
		context['housepd'] = ''
	return render(request, 'index.html', context)


def huxing(request):
	context = {}
	context['huxing'] = '/static/images/huxing.png'
	return render(request, 'huxing.html', context)

'''
def huxing(request):
	context = {}
	if request.POST:
		context['huxing'] = '/static/images/huxing.png'
		context['display'] = 'display:block;'
	else:
		context['huxing'] = '/'
		context['display'] = 'display:none;'
	return render(request, 'huxing.html', context)

def huxing(request):
	context = {}
	if request.POST:
		execfile('spider/zyHuxing.py')
		context['huxing'] = 'done'
	else:
		context['huxing'] = ''
	return render(request, 'huxing.html', context)
'''
def mianji(request):
	context = {}
	context['mianji'] = '/static/images/mianji.png'
	return render(request, 'mianji.html', context)

def daikan(request):
	context = {}
	context['daikan'] = '/static/images/follow.png'
	return render(request, 'daikan.html', context)

def chaoxiang(request):
	context = {}
	context['chaoxiang'] = '/static/images/chaoxiang.png'
	return render(request, 'chaoxiang.html', context)

def cluster(request):
	context = {}
	context['cluster'] = '/static/images/cluster.png'
	return render(request, 'cluster.html', context)