#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import OrderSeparate,OrderSeparateFeedBack,Shop
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def orderSeparateAddInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _name = request.REQUEST.get('name')
    _headImage = request.REQUEST.get('headImage')

    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _headImage == None or _headImage == '':
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
    _name = str(_name)
    _headImage = str(_headImage)

    if  orderSeparate.everSetInfo == True:
        response['code'] = -1
        response['errorMsg'] = '已经设置过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    orderSeparate.name = _name
    orderSeparate.headImage = _headImage
    orderSeparate.everSetInfo = True
    orderSeparate.save()
    response['code'] = 0
    response['data'] = {'type':'2','orderSeparateId':str(orderSeparate .id)}
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def orderSeparateGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['orderSeparateName'] = orderSeparate.name.encode('utf-8')
    response_data['orderSeparateTelephone'] = orderSeparate.telephone
    response_data['orderSeparateHeadImage'] = orderSeparate.headImage
    if orderSeparate.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(orderSeparate.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def orderSeparateAlterInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
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


    orderSeparate.name = _name
    orderSeparate.headImage = _headImage
    orderSeparate.save()

    response['code'] = 0
    response_data = {}
    response_data['orderSeparateName'] = orderSeparate.name.encode('utf-8')
    response_data['orderSeparateTelephone'] = orderSeparate.telephone
    response_data['orderSeparateHeadImage'] = orderSeparate.headImage
    if orderSeparate.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(orderSeparate.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterOrderSeparateName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')


    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    orderSeparate.name = _name
    orderSeparate.save()

    response['code'] = 0
    response_data = {}
    response_data['orderSeparateName'] = orderSeparate.name.encode('utf-8')
    response_data['orderSeparateTelephone'] = orderSeparate.telephone
    response_data['orderSeparateHeadImage'] = orderSeparate.headImage
    if orderSeparate.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(orderSeparate.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterOrderSeparateHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    orderSeparate.headImage = _headImage
    orderSeparate.save()

    response['code'] = 0
    response_data = {}
    response_data['orderSeparateName'] = orderSeparate.name.encode('utf-8')
    response_data['orderSeparateTelephone'] = orderSeparate.telephone
    response_data['orderSeparateHeadImage'] = orderSeparate.headImage
    if orderSeparate.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(orderSeparate.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def orderSeparateFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    orderSeparateFeedback = OrderSeparateFeedBack(orderSeparate = orderSeparate, msg = _msg, date =datetime.datetime.now())
    orderSeparateFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def orderSeparateUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if orderSeparate.clientID != _clientID:
        orderSeparate.clientID = _clientID
        orderSeparate.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def orderSeparateUpdateDeviceToken(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _orderSeparateId = request.session.get('orderSeparateId')
    if not _orderSeparateId:
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
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _deviceToken = request.REQUEST.get('deviceToken')
    if _deviceToken == None or _deviceToken == '':
        response['code'] = -1
        response['errorMsg'] = '请上传deviceToken'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if orderSeparate.deviceToken != _deviceToken:
        orderSeparate.deviceToken = _deviceToken
        orderSeparate.save()
    response['code'] = 0
    response['data'] = {'deviceToken':_deviceToken}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
