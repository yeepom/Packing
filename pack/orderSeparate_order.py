__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import OrderSeparate,OrderSku
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist
from pack.tasks import orderSeparatePushMessage
import pytz
from pack.pack_push_2_shop import pushAPNToShop,pushMessageToSingle

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def orderSeparateGetCurrentOrderSkuList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = []
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
        orderSeparate = OrderSeparate.objects.select_related().get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != orderSeparate.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    if orderSeparate.category == None:
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response),content_type="application/json")

    orderSkuQuery = OrderSku.objects.filter(status='2').filter(orderSeparateId = str(orderSeparate.id)).order_by('id')
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
            _orderSku['tableId'] = orderSku.tableId
            _orderSku['tableNumber'] = orderSku.tableNumber
            orderSkuList.append(_orderSku)
        response['code'] = 0
        response['data'] = orderSkuList
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def orderSeparateFinishOrderSkuList(request):
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

        if orderSku.status == '2' and orderSku.categoryType =='0' and orderSku.orderSeparateId == str(orderSeparate.id):
            orderSku.status = '4'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='1' and orderSku.orderSeparateId == str(orderSeparate.id):
            orderSku.status = '6'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='2' and orderSku.orderSeparateId == str(orderSeparate.id):
            orderSku.status = '8'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='10' and orderSku.orderSeparateId == str(
            orderSeparate.id):
            orderSku.status = '4'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='11' and orderSku.orderSeparateId == str(
                orderSeparate.id):
            orderSku.status = '6'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='12' and orderSku.orderSeparateId == str(
                orderSeparate.id):
            orderSku.status = '8'
            orderSku.save()
        elif orderSku.status == '2' and orderSku.categoryType =='13' and orderSku.orderSeparateId == str(
                orderSeparate.id):
            orderSku.status = '10'
            orderSku.save()
        else:
            response['code'] = -1
            response['errorMsg'] = '请刷新后重新操作'
            return HttpResponse(json.dumps(response),content_type="application/json")
    orderSeparatePushMessage.delay(_orderSkuList)
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")

# @csrf_exempt
# def testPush(request):
#     pushRst = pushMessageToSingle("bc8b02456bb6cc48842e2684e1fc8687",'{"method":"pushNewOrdersToSaler"}')
#     print pushRst
#     return HttpResponse(pushRst)
#
@csrf_exempt
def testPushIOS(request):
    pushRst = pushAPNToShop("db6796bef6cc77cb3501e434076662856afc2a90ede564bbfb98db69f49b471d",'0',
                            '{"method":"pushNewOrderSkusToOrderSeparate"}')
    return HttpResponse(pushRst)
#
# @csrf_exempt
# def testPushViaClientID(request):
#     pushRst = pushMessageToSingle("dcd7b53c18bc756642d883f192ffc063",'{"method":"pushNewOrdersToSaler"}')
#     return HttpResponse(pushRst)
