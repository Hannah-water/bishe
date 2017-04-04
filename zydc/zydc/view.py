#-*-coding:utf-8 -*-

from django.shortcuts import render

def index(request):
	context = {}
	return render(request, 'index.html')

def huxing(request):
	context = {}
	context['huxing'] = '/static/images/huxing.png'
	return render(request, 'huxing.html', context)

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