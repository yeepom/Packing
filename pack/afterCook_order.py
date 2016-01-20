__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import AfterCook,OrderSku
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist
from pack.tasks import afterCookPushMessage

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def afterCookGetCurrentOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = []
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.select_related().get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    if afterCook.category == None:
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response),content_type="application/json")

    orderSkuQuery = OrderSku.objects.filter(status='6').filter(afterCookId = str(afterCook.id)).order_by('id')
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
def afterCookFinishOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.select_related().get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderSkuList = request.REQUEST.getlist('orderSkuList[]')

    if _orderSkuList == None or _orderSkuList == '':
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

        if orderSku.status == '6' and orderSku.afterCookId == str(afterCook.id):
            orderSku.status = '8'
            orderSku.save()
        else:
            response['code'] = -1
            response['errorMsg'] = 'orderSku状态错误'
            return HttpResponse(json.dumps(response),content_type="application/json")
    afterCookPushMessage.delay(_orderSkuList)
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")
