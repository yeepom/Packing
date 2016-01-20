#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import Shop,Order,OrderSku,Waiter,User
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from pack.pack_push_2_user import pushAPNToUser
import pytz

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def PushAPN(request):
    _deviceToken = request.REQUEST.get("deviceToken")
    print '1111'
    pushAPNToUser(_deviceToken,'1000','350')
    return HttpResponse('yes')

@csrf_exempt
def getShopOrderListWithTable(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        shop = Shop.objects.get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != shop.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _tableId = request.REQUEST.get('tableId')
    _orderId = request.REQUEST.get('orderId')
    _limit = request.REQUEST.get('limit',20)
    _limit = int(_limit)
    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _tableId = str(_tableId)
    _orderId = str(_orderId)
    if _orderId == '0':
        orderQuery = Order.objects.filter(tableId =_tableId).order_by('id')
    else:
        orderQuery = Order.objects.filter(tableId =_tableId).filter(id__lt = _orderId).order_by('id')
    orders = orderQuery.reverse()[0:0+_limit]
    orderList = []
    for order in orders:
        _order = {}
        _order['orderId'] = order.id
        _tableInfo = {}
        _tableInfo['tableId'] = order.tableId
        _tableInfo['tableNumber'] = order.tableNumber
        _order['tableInfo'] = _tableInfo

        _order['tableNumber'] = order.tableNumber
        _priceTotal = float(order.priceTotal)
        _order['priceTotal'] = str(_priceTotal)
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')
        _order['status'] = order.status
        orderList.append(_order)
    response['code'] = 0
    response['data'] = orderList
    return HttpResponse(json.dumps(response),content_type = "application/json")


@csrf_exempt
def getShopOrderDetail(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        shop = Shop.objects.get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != shop.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderId = request.REQUEST.get('orderId')
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取订单详情失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    try:
        order = Order.objects.select_related().get(id = _orderId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取订单详情失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _order = {}
    # _orderInfo = {}
    _order['orderId'] = order.id
    _order['priceTotal'] = float(order.priceTotal)
    _order['status'] = order.status
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')

    _tableInfo = {}
    _tableInfo['tableId'] = order.tableId
    _tableInfo['tableNumber'] = order.tableNumber
    _order['tableInfo'] = _tableInfo

    if order.userId =='':
        _order['userInfo'] = ''
    else:
        try:
            user = User.objects.get(id = order.userId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取用户消息失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        _userInfo = {}
        _userInfo['userId'] = str(user.id)
        _userInfo['userName'] = user.name
        _userInfo['userHeadImage'] = user.headImage
        _userInfo['userTelephone'] = user.telephone
        _order['userInfo'] = _userInfo
    _skuList = []
    orderSkuQuery = OrderSku.objects.filter(order__id = order.id).order_by('id')
    for orderSku in orderSkuQuery:
        _sku = {}
        _sku['orderSkuId'] = orderSku.id
        _sku['skuId'] = orderSku.skuId
        _sku['skuName'] = orderSku.skuName.encode('utf-8')
        _sku['skuPrice'] = float(orderSku.skuPrice)
        _sku['skuSizeName'] = str(orderSku.skuSizeName)
        _sku['skuQuantity'] = float(orderSku.skuQuantity)
        _sku['skuStatus'] = orderSku.status
        _skuList.append(_sku)
    _order['orderSkuList'] = _skuList
    try:
        waiter = Waiter.objects.get(id = str(order.waiterId))
    except ObjectDoesNotExist:
        logger.info('查找waiter失败')
        response['data'] = _order
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        _waiter = {}
        _waiter['waiterId']=waiter.id
        _waiter['waiterName'] = waiter.name
        _waiter['waiterTelephone'] = waiter.telephone
        _waiter['waiterHeadImage'] = waiter.headImage
        _order['waiterInfo'] = _waiter
        response['data'] = _order
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def getShopDoingOrderList(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        shop = Shop.objects.get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != shop.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderId = request.REQUEST.get('orderId')
    _limit = request.REQUEST.get('limit',20)
    _limit = int(_limit)

    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _orderId = str(_orderId)
    if _orderId == '0':
        orderQuery = Order.objects.filter(status = '0').order_by('id')
    else:
        orderQuery = Order.objects.filter(status = '0').filter(id__lt = _orderId).order_by('id')
    orders = orderQuery.reverse()[0:0+_limit]
    orderList = []
    for order in orders:
        _order = {}
        _order['orderId'] = order.id
        _order['tableNumber'] = order.tableNumber
        _priceTotal = float(order.priceTotal)
        _order['priceTotal'] = str(_priceTotal)
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')
        _order['status'] = order.status
        _tableInfo = {}
        _tableInfo['tableId'] = order.tableId
        _tableInfo['tableNumber'] = order.tableNumber
        _order['tableInfo'] = _tableInfo
        orderList.append(_order)
    response['code'] = 0
    response['data'] = orderList
    return HttpResponse(json.dumps(response),content_type = "application/json")
