#coding=UTF-8

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from graph.get_fig_info import *
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

import yaml

# Create your views here.
def home(request):
    print 'Get a request!'
    return render(request, 'index.html')

# @ensure_csrf_cookie
# def note(request):
#     print 'Get a note!'
#     print request
#     note_data = {'data': ['hello'], 'title': 'test', 'table': False}
#     return render(request, 'notes.html', note_data)

@csrf_exempt
def note(request):
    print 'Get a note!'
    return render(request, 'notes.html', data)


# @ensure_csrf_cookie
@csrf_exempt
def add_note(request):
    if request.method == "POST":
        print 'Get into add_note!'
        # print request.POST.get('data')
        # result = request.body
        result = yaml.safe_load(request.body)
        # print result
        # return render(request, 'notes.html', result)
        html =  render(request, 'notes.html', result)
        return HttpResponse(html)
        # return HttpResponse(json.dumps({'status': 1, 'html': html}))
    else:
        return HttpResponse(json.dumps({'status': 0}))


def nanke(request):
    input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data_processing/data/nanke/output_sentense_10.dat'
    # input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data/nanke/nanke_10.dat'

    graph_title = u'男科问题画像'
    graph_param = load_data(input_path, graph_title)
    
    init_info = {}
    # init_info['graph_title'] = graph_title
    init_info['graph_data'] = mark_safe(graph_param)
    return render(request, 'home.html', init_info)

def fuke(request):
    input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data_processing/data/fuke/output_sentense_10.dat'
    # input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data/nanke/nanke_10.dat'

    graph_title = u'妇科问题画像'
    graph_param = load_data(input_path, graph_title)
    
    init_info = {}
    # init_info['graph_title'] = graph_title
    init_info['graph_data'] = mark_safe(graph_param)
    return render(request, 'home.html', init_info)

def obesity(request):
    input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data_processing/data/obesity/output_sentense_10.dat'
    
    graph_title = u'减肥问题画像'
    graph_param = load_data(input_path, graph_title)
    
    init_info = {}
    # init_info['graph_title'] = graph_title
    
    init_info['graph_data'] = mark_safe(graph_param)
    return render(request, 'home.html', init_info)

def skin(request):
    input_path = '/home/hty136208/projects/django_test/Echarts_show_word/data_processing/data/skin/output_sentense_10.dat'
    
    graph_title = u'皮肤病问题画像'
    graph_param = load_data(input_path, graph_title)
   
    init_info = {}
    # init_info['graph_title'] = graph_title
    
    init_info['graph_data'] = mark_safe(graph_param)
    
    return render(request, 'home.html', init_info)


def load_data(path, title):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except Exception, e:
        print 'Wrong input path!'
        raise e
    return Fig_param(data, title).get()