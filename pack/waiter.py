#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import Waiter,WaiterFeedBack
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def waiterAddInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _name = request.REQUEST.get('name')
    _headImage = request.REQUEST.get('headImage')

    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _headImage == None or _headImage == '':
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
    _name = str(_name)
    _headImage = str(_headImage)

    if  waiter.everSetInfo == True:
        response['code'] = -1
        response['errorMsg'] = '已经设置过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    waiter.name = _name
    waiter.headImage = _headImage
    waiter.everSetInfo = True
    waiter.save()
    response['data'] = {'type':'1','waiterId':str(waiter.id)}
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def waiterGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['waiterName'] = waiter.name.encode('utf-8')
    response_data['waiterTelephone'] = waiter.telephone
    response_data['waiterHeadImage'] = waiter.headImage
    if waiter.shop == None:
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        response_shopInfo = {}
        response_shopInfo['shopId'] = str(waiter.shop.id)
        response_shopInfo['shopName'] = str(waiter.shop.name)
        response_shopInfo['shoptelephone'] = str(waiter.shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def waiterAlterInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _name = request.REQUEST.get('name')
    _headImage = request.REQUEST.get('headImage')



    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _name = str(_name)
    _headImage = str(_headImage)
    waiter.name = _name
    waiter.headImage = _headImage
    waiter.save()

    response['code'] = 0
    response_data = {}
    response_data['waiterName'] = waiter.name.encode('utf-8')
    response_data['waiterTelephone'] = waiter.telephone
    response_data['waiterHeadImage'] = waiter.headImage
    if waiter.shop == None:
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        response_shopInfo = {}
        response_shopInfo['shopId'] = str(waiter.shop.id)
        response_shopInfo['shopName'] = str(waiter.shop.name)
        response_shopInfo['shoptelephone'] = str(waiter.shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def alterWaiterName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')


    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    waiter.name = _name
    waiter.save()

    response['code'] = 0
    response_data = {}
    response_data['waiterName'] = waiter.name.encode('utf-8')
    response_data['waiterTelephone'] = waiter.telephone
    response_data['waiterHeadImage'] = waiter.headImage
    if waiter.shop == None:
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        response_shopInfo = {}
        response_shopInfo['shopId'] = str(waiter.shop.id)
        response_shopInfo['shopName'] = str(waiter.shop.name)
        response_shopInfo['shoptelephone'] = str(waiter.shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterWaiterHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    waiter.headImage = _headImage
    waiter.save()

    response['code'] = 0
    response_data = {}
    response_data['waiterName'] = waiter.name.encode('utf-8')
    response_data['waiterTelephone'] = waiter.telephone
    response_data['waiterHeadImage'] = waiter.headImage
    if waiter.shop == None:
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        response_shopInfo = {}
        response_shopInfo['shopId'] = str(waiter.shop.id)
        response_shopInfo['shopName'] = str(waiter.shop.name)
        response_shopInfo['shoptelephone'] = str(waiter.shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def waiterFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    waiterFeedback = WaiterFeedBack(waiter = waiter, msg = _msg , date = datetime.datetime.now())
    waiterFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def waiterUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if waiter.clientID != _clientID:
        waiter.clientID = _clientID
        waiter.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
