from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import redis
import json
from json2html import *


def get_item_list(port):
    item_list = []
    queue = redis.StrictRedis('localhost', port)
    for key in queue.scan_iter():
        item = json.loads(queue.execute_command('JSON.GET', key))
        item_list.append(json2html.convert(json=item))
    context = {
        'item_list': item_list,
    }
    return context


def grading_queue(request):
    context = get_item_list(6379)
    template = loader.get_template('application/queue.html')
    return render(request, 'application/queue.html', context)


def dedup_queue(request):
    context = get_item_list(6380)
    template = loader.get_template('application/queue.html')
    return render(request, 'application/queue.html', context)


def poison_queue(request):
    context = get_item_list(6381)
    template = loader.get_template('application/queue.html')
    return render(request, 'application/queue.html', context)
