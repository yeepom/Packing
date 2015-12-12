#encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader,Context
import base64,urllib,urllib2,sys,re,json,random,time
from pack.xmltojson import xmltojson

def index(request):
    userAgent = request.META['HTTP_USER_AGENT']
    result_iOS = userAgent.find('iPhone')
    result_Android = userAgent.find('Android')
    result_WindowsPhone = userAgent.find('Windows Phone')
    result = 0
    #result = 0，请求来自于电脑；result = 1，请求来自手机
    if result_iOS != -1:
        result = 1
    if result_Android != -1:
        result = 1
    if result_WindowsPhone != -1:
        result = 1
    if result == 0:
        t = loader.get_template('index.html')
        c = Context({})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('index.html')
        c = Context({})
        return HttpResponse(t.render(c))


def shopProtocol(request):
    t = loader.get_template('shopProtocol.html')
    c = Context({})
    return HttpResponse(t.render(c))



def userProtocol(request):
    t = loader.get_template('userProtocol.html')
    c = Context({})
    return HttpResponse(t.render(c))


