__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import BeforeCook,OrderSku,Cook
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist
from pack.tasks import beforeCookPushMessage
reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def beforeCookGetCurrentOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = []
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.select_related().get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    if beforeCook.category == None:
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response),content_type="application/json")

    orderSkuQuery = OrderSku.objects.filter(status='4').filter(beforeCookId = str(beforeCook.id))
    if not orderSkuQuery.exists():
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        orderSkuList = []
        for orderSku in orderSkuQuery:
            _orderSku = {}
            _orderSku['orderSkuId'] = orderSku.id
            _orderSku['skuId'] = orderSku.skuId
            _orderSku['skuName'] = orderSku.skuName
            _orderSku['skuPrice'] = float(orderSku.skuPrice)
            _orderSku['skuSizeName'] = orderSku.skuSizeName
            _orderSku['skuQuantity'] = orderSku.skuQuantity
            _orderSku['skuSizeStatus'] = orderSku.status
            _orderSku['orderSeparateId'] = orderSku.orderSeparateId
            _orderSku['orderSeparateName'] = orderSku.orderSeparateName
            _orderSku['tableId'] = orderSku.tableId
            _orderSku['tableNumber'] = orderSku.tableNumber
            orderSkuList.append(_orderSku)
        response['code'] = 0
        response['data'] = orderSkuList
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def beforeCookFinishOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.select_related().get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderSkuList = request.REQUEST.getlist('orderSkuList[]')

    if _orderSkuList == None or _orderSkuList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入订单id'
        return HttpResponse(json.dumps(response),content_type="application/json")

    beforeCookPushMessage.delay(_orderSkuList)

    for _orderSkuId in _orderSkuList:
        _orderSkuId = str(_orderSkuId)
        try:
            orderSku = OrderSku.objects.get(id = _orderSkuId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '查询orderSku失败'
            return HttpResponse(json.dumps(response),content_type="application/json")

        if orderSku.status == '4' and orderSku.beforeCookId == str(beforeCook.id):
            orderSku.status = '6'
            orderSku.save()
        else:
            response['code'] = -1
            response['errorMsg'] = 'orderSku状态错误'
            return HttpResponse(json.dumps(response),content_type="application/json")
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")


#
# @csrf_exempt
# def beforeCookGetCookList(request):
#     logger = logging.getLogger('Pack.app')
#     response = {}
#     response['data'] = []
#     response['errorMsg'] = ""
#     _beforeCookId = request.session.get('beforeCookId')
#     if not _beforeCookId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         beforeCook = BeforeCook.objects.select_related().get(id = _beforeCookId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != beforeCook.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     category = beforeCook.category
#     orderSkuQuery = OrderSku.objects.filter(categoryId = category.id).filter(status = '6')
#     cookList = category.cook_set.all()
#     _cookList = []
#     for cook in cookList:
#         _cook = {}
#         _cook['cookId'] = cook.id
#         _cook['cookName'] = cook.name
#         _cook['cookTelephone'] = cook.telephone
#         _cook['orderSkuCount'] = orderSkuQuery.filter(cookId = cook.id).count()
#         _cookList.append(_cook)
#     response['code'] = 0
#     response['data'] = _cookList
#     return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#
#
# @csrf_exempt
# def beforeCookDispatchSingleOrderSku(request):
#     logger = logging.getLogger('Pack.app')
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     _beforeCookId = request.session.get('beforeCookId')
#     if not _beforeCookId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         beforeCook = BeforeCook.objects.select_related().get(id = _beforeCookId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != beforeCook.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _orderSkuId = request.REQUEST.get('orderSkuId')
#     _cookId = request.REQUEST.get('cookId')
#     _cookName = request.REQUEST.get('cookName')
#     if _orderSkuId == None or _orderSkuId == '':
#         response['code'] = -1
#         response['errorMsg'] = '获取orderSkuId失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _cookId == None or _cookId == '':
#         response['code'] = -1
#         response['errorMsg'] = '获取cookId失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _cookName == None or _cookName == '':
#         response['code'] = -1
#         response['errorMsg'] = '获取cookName失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     try:
#         orderSku = OrderSku.objects.get(id = str(_orderSkuId))
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '查询orderSku失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     if orderSku.status == '4' and orderSku.beforeCookId == str(beforeCook.id):
#         orderSku.status = '6'
#         orderSku.cookId = str(_cookId)
#         orderSku.cookName = str(_cookName)
#         orderSku.save()
#     logger.info('==================')
#     beforeCookPushMessage(_orderSkuId)
#     response['code'] = 0
#     return HttpResponse(json.dumps(response),content_type="application/json")
