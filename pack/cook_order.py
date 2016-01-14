__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Cook,OrderSku
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def cookGetOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = []
    response['errorMsg'] = ""
    _cookId = request.session.get('cookId')
    if not _cookId:
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
        cook = Cook.objects.select_related().get(id = _cookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != cook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    if cook.category == None:
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response),content_type="application/json")

    orderSkuQuery = OrderSku.objects.filter(cookId = str(cook.id))
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