# -*- coding: utf-8 -*-
import os
import threading
from django.http import JsonResponse
from Spider.NewsUrlSpider import begincollect
from Spider.NewsDetailSpider import begindetailcollect
from Spider import NewsUrlSpider, NewsDetailSpider
from news_api.models import spiderstate, urlcollect


def beginUrlSpider(request):
    '''
        启动新闻URL采集系统，前端获取间隔时间
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=begincollect, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        spiderstate.objects.filter(spiderid=1).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def beginDetailSpider(request):
    '''
        启动新闻详情页内容采集系统
    '''
    if request.method == "GET":
        time = request.GET.get('time')
        oritime = request.GET.get('oritime')
        t = threading.Thread(target=begindetailcollect, kwargs={'time': time})
        t.setDaemon(True)
        t.start()
        # begindetailcollect(time)
        spiderstate.objects.filter(spiderid=2).update(status=1, interval=oritime)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def closeSpiderThread(request):
    '''
        关闭爬虫系统
    '''
    if request.method == "GET":
        servename = request.GET.get('servename')
        if servename == 'url':
            spiderstate.objects.filter(spiderid=1).update(status=0, interval='')
            NewsUrlSpider.endsched()
        elif servename == 'detail':
            spiderstate.objects.filter(spiderid=2).update(status=0, interval='')
            NewsDetailSpider.endsched()
        # getpidandkill(servename)
        return JsonResponse({"status": "200", 'message': 'Success.'})
    return JsonResponse({"status": "200", 'message': 'Fail.'})


def getSpiderPageData(request):
    '''
        获取爬虫系统管理页统计数据
    '''
    if request.method == "GET":
        statelist = spiderstate.objects.all()
        urllist = urlcollect.objects.all()
        urlloglist = dict()
        detaillist = dict()
        original_data_path = "Spider/Detaillogs/"
        files = os.listdir(original_data_path)
        for file in files:
            if str(file) == 'log.log':
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('E:\\python_project\\NewsRecommends-master\\FinalProject\\newsapi\\Spider\\Detaillogs', file)

            urlloglist[file] = {
                'time': time,
                'filepath': filepath
            }
        original_data_path = "Spider/Urllogs/"
        files = os.listdir(original_data_path)
        for file in files:
            if str(file) == 'log.log':
                pass
            time = file[8:].replace("_", ' ')
            time = time[:13] + ':' + time[14:16] + ':' + time[17:]
            filepath = os.path.join('E:\\python_project\\NewsRecommends-master\\FinalProject\\newsapi\\Spider\\Urllogs', file)
            detaillist[file] = {
                'time': time,
                'filepath': filepath
            }
        statistical = dict()
        for url in urllist:
            if statistical.get(url.time) == None:
                statistical[url.time] = 1
            else:
                statistical[url.time] = statistical[url.time] + 1
        spiderstatelist = dict()
        for state in statelist:
            spiderstatelist[state.spiderid] = [state.status, state.interval]
        data = {
            'spiderstatelist': spiderstatelist,
            'statistical': statistical,
            'urlloglist': urlloglist,
            'detaillist': detaillist,

        }
        return JsonResponse({"status": "200", 'message': data})
