__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Serve,OrderSku
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def serveGetCurrentOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = []
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    if serve.shopId =='':
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    orderSkuQuery = OrderSku.objects.filter(status='8').filter(serveId = str(serve.id))
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
            _orderSku['beforeCookId'] = orderSku.beforeCookId
            _orderSku['beforeCookName'] = orderSku.beforeCookName
            _orderSku['afterCookId'] = orderSku.afterCookId
            _orderSku['afterCookName'] = orderSku.afterCookName
            _orderSku['tableId'] = orderSku.tableId
            _orderSku['tableNumber'] = orderSku.tableNumber
            orderSkuList.append(_orderSku)
        response['code'] = 0
        response['data'] = orderSkuList
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def serveFinishOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderSkuList = request.REQUEST.getlist('orderSkuList[]')

    if _orderSkuList == []:
        response['code'] = -1
        response['errorMsg'] = '请输入订单id'
        return HttpResponse(json.dumps(response),content_type="application/json")

    for _orderSkuId in _orderSkuList:
        _orderSkuId = str(_orderSkuId)
        try:
            orderSku = OrderSku.objects.get(id = _orderSkuId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '查询orderSku失败'
            return HttpResponse(json.dumps(response),content_type="application/json")

        if orderSku.status == '8' and orderSku.serveId == str(serve.id):
            orderSku.status = '10'
            orderSku.save()
        else:
            response['code'] = -1
            response['errorMsg'] = 'orderSku状态错误'
            return HttpResponse(json.dumps(response),content_type="application/json")
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")
