__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import Order,Waiter,OrderSku,Table,OrderRecord,User,OrderSku
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from pack.pack_push_2_user import pushAPNToUser,pushMessageToSingle
from pack.tasks import waiterPushMessage
import pytz

reload(sys)
sys.setdefaultencoding('utf8')


@csrf_exempt
def submitOrder(request):
    logger = logging.getLogger('Pack.app')
    logger.info(request)
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
        waiter = Waiter.objects.select_related().get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _tableId = request.REQUEST.get('tableId')
    _priceTotal = request.REQUEST.get('priceTotal')
    _categoryIdList = request.REQUEST.getlist('categoryIdList[]')
    _categoryTypeList = request.REQUEST.getlist('categoryTypeList[]')
    _skuIdList = request.REQUEST.getlist('skuIdList[]')
    _skuNameList = request.REQUEST.getlist('skuNameList[]')
    _skuQuantityList = request.REQUEST.getlist('skuQuantityList[]')
    _skuSizeNameList = request.REQUEST.getlist('skuSizeNameList[]')
    _skuPriceList = request.REQUEST.getlist('skuPriceList[]')


    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if _priceTotal == None or _priceTotal == '':
        response['code'] = -1
        response['errorMsg'] = '获取总计价格失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _categoryIdList == None or _categoryIdList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _categoryTypeList == None or _categoryTypeList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuIdList == None or _skuIdList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuNameList == None or _skuNameList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuQuantityList == None or _skuQuantityList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuSizeNameList == None or _skuSizeNameList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuPriceList == None or _skuPriceList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")

    logger.info(len(_categoryIdList))
    logger.info(len(_categoryTypeList))
    logger.info(len(_skuIdList))
    logger.info(len(_skuNameList))
    logger.info(len(_skuSizeNameList))
    logger.info(len(_skuQuantityList))
    logger.info(len(_skuPriceList))
    if len(_categoryIdList) != len(_skuIdList) or len(_categoryIdList) != len(_categoryTypeList)\
            or len(_categoryIdList) != len(_skuNameList) \
            or len(_categoryIdList)!=len(_skuQuantityList) or len(_categoryIdList) != len(_skuSizeNameList) \
            or len(_categoryIdList) != len(_skuPriceList):
        response['code'] = -1
        response['errorMsg'] = '对应关系错误'
        return HttpResponse(json.dumps(response),content_type="application/json")

    try:
        table = Table.objects.select_related().get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取餐桌信息失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if table.status == '0':
        response['code'] = -1
        response['errorMsg'] = '请先锁定餐桌，然后下单'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif table.status == '2' and table.waiterId == str(waiter.id):
        order = Order(shopId = str(waiter.shop.id),waiterId=str(waiter.id),waiterName=str(waiter.name),
                priceTotal =str(_priceTotal),tableId = str(table.id), tableNumber = str(table.number),status = '0',
                date =datetime.datetime.now())
        order.save()
        table.status = '3'
        table.save()
        submitRecord = u'点菜成功，订单号为：'.encode('utf-8')
        submitRecord = submitRecord + str(order.id)
        submitRecord = submitRecord + u'，桌号为：'.encode('utf-8')
        submitRecord = submitRecord + str(table.number)
        record = OrderRecord(record = submitRecord,order=order,date = datetime.datetime.now())
        record.save()

        _orderSkuList = []
        for index in range(len(_categoryIdList)):
            categoryId = _categoryIdList[index]
            categoryType = _categoryTypeList[index]
            skuId = _skuIdList[index]
            skuName = _skuNameList[index]
            skuQuantity = _skuQuantityList[index]
            skuSize = _skuSizeNameList[index]
            skuPrice = _skuPriceList[index]
            _orderSkuList.append(OrderSku(order = order,shopId = str(waiter.shop.id),tableId = str(table.id),
                                          tableNumber = str(table.number),categoryId = str(categoryId),
                                          categoryType = str(categoryType),
                                          skuId=(skuId),
                                          skuName=str(skuName),
                                          skuQuantity=int(skuQuantity),
                                          skuSizeName = str(skuSize),
                                          skuPrice = float(skuPrice),status = '0'))
        OrderSku.objects.bulk_create(_orderSkuList)
        waiterPushMessage.delay(str(order.id))

        response_data = {}
        _order = {}
        _order['orderId'] = order.id
        _order['priceTotal'] = float(order.priceTotal)
        _order['status'] = order.status
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.strftime('%Y/%m/%d %H:%M:%S')

        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number.encode('utf-8')
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        _order['tableInfo'] = _table
        response_data['tableInfo'] = _table

        _waiter_Info = {}
        _waiter_Info['waiterId'] = str(order.waiterId)
        _waiter_Info['waiterName'] = str(order.waiterName)
        _order['waiterInfo'] = _waiter_Info
        response_data['waiterInfo'] = _waiter_Info

        _skuList = []
        orderSkuQuery = order.ordersku_set.all().order_by('-id')
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
        response_data['orderInfo'] = _order
        response['data'] = response_data
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type = "application/json")
    elif table.status == '2' and table.waiterId != str(waiter.id):
        response['code'] = -1
        response['errorMsg'] = '该餐桌被其他服务员锁定'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif table.status == '3':
        response['code'] = -1
        response['errorMsg'] = '该餐桌正在忙碌，无法下单'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def addSkusWithOrder(request):
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
        waiter = Waiter.objects.select_related().get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderId = request.REQUEST.get('orderId')
    _priceTotal = request.REQUEST.get('priceTotal')
    _categoryIdList = request.REQUEST.getlist('categoryIdList[]')
    _categoryTypeList = request.REQUEST.getlist('categoryTypeList[]')
    _skuIdList = request.REQUEST.getlist('skuIdList[]')
    _skuNameList = request.REQUEST.getlist('skuNameList[]')
    _skuQuantityList = request.REQUEST.getlist('skuQuantityList[]')
    _skuSizeNameList = request.REQUEST.getlist('skuSizeNameList[]')
    _skuPriceList = request.REQUEST.getlist('skuPriceList[]')

    if _priceTotal == None or _priceTotal == '':
        response['code'] = -1
        response['errorMsg'] = '获取总计价格失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _categoryIdList == None or _categoryIdList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _categoryTypeList == None or _categoryTypeList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuIdList == None or _skuIdList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuNameList == None or _skuNameList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuQuantityList == None or _skuQuantityList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuSizeNameList == None or _skuSizeNameList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _skuPriceList == None or _skuPriceList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入对应关系'
        return HttpResponse(json.dumps(response),content_type="application/json")

    if len(_categoryIdList) != len(_skuIdList) or len(_categoryIdList) != len(_categoryTypeList)\
            or len(_categoryIdList) != len(_skuNameList) \
            or len(_categoryIdList)!=len(_skuQuantityList) or len(_categoryIdList) != len(_skuSizeNameList) \
            or len(_categoryIdList) != len(_skuPriceList):
        response['code'] = -1
        response['errorMsg'] = '对应关系错误'
        return HttpResponse(json.dumps(response),content_type="application/json")

    try:
        order = Order.objects.get(id = _orderId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取餐桌信息失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    print order.id
    print '0------0'
    print order.status
    if str(order.status) == '0' and str(order.waiterId) == str(waiter.id):
        priceTotal = float(order.priceTotal) + float(_priceTotal)
        order.priceTotal = priceTotal
        order.save()
        submitRecord = u'加菜成功'.encode('utf-8')
        record = OrderRecord(record = submitRecord,order=order,date = datetime.datetime.now())
        record.save()

        _orderSkuList = []
        for index in range(len(_categoryIdList)):
            categoryId = _categoryIdList[index]
            categoryType = _categoryTypeList[index]
            skuId = _skuIdList[index]
            skuName = _skuNameList[index]
            skuQuantity = _skuQuantityList[index]
            skuSize = _skuSizeNameList[index]
            skuPrice = _skuPriceList[index]
            _orderSkuList.append(OrderSku(order = order,shopId = str(waiter.shop.id),tableId = str(order.tableId),
                                          tableNumber = str(order.tableNumber),categoryId=str(categoryId),
                                          categoryType = str(categoryType),
                                          skuId=str(skuId),
                                          skuName=str(skuName), skuQuantity=int(skuQuantity), skuSizeName = str(skuSize),
                                          skuPrice = float(skuPrice),status = '0'))
        OrderSku.objects.bulk_create(_orderSkuList)
        waiterPushMessage.delay(str(order.id))

        try:
            table = Table.objects.select_related().get(id = str(order.tableId))
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取餐桌信息失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_data = {}
        _order = {}
        _order['orderId'] = order.id
        _order['priceTotal'] = float(order.priceTotal)
        _order['status'] = order.status
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.strftime('%Y/%m/%d %H:%M:%S')

        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number.encode('utf-8')
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        _order['tableInfo'] = _table
        response_data['tableInfo'] = _table

        _waiter_Info = {}
        _waiter_Info['waiterId'] = str(order.waiterId)
        _waiter_Info['waiterName'] = str(order.waiterName)
        _order['waiterInfo'] = _waiter_Info
        response_data['waiterInfo'] = _waiter_Info

        _skuList = []
        orderSkuQuery = order.ordersku_set.all().order_by('-id')
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
        response_data['orderInfo'] = _order
        response['data'] = response_data
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type = "application/json")

    else:
        response['code'] = -1
        response['errorMsg'] = ''
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def waiterCancelOrderSku(request):
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
        waiter = Waiter.objects.select_related().get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderSkuId = request.REQUEST.get('orderSkuId')

    if _orderSkuId == None or _orderSkuId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入订单id'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _orderSkuId = str(_orderSkuId)
    logger.info(_orderSkuId)
    orderSkuQuery = OrderSku.objects.filter(orderSkuId = _orderSkuId)
    if orderSkuQuery[0].status == '6':
        response['code'] = -1
        response['errorMsg'] = '厨师正在做菜，无法取消'
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif orderSkuQuery[0].status == '8':
        response['code'] = -1
        response['errorMsg'] = '上菜员正在上菜，无法取消'
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif orderSkuQuery[0].status == '10':
        response['code'] = -1
        response['errorMsg'] = '已经上过菜啦'
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif orderSkuQuery[0].status == '200':
        response['code'] = -1
        response['errorMsg'] = '该菜品已经取消'
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        orderSku = orderSkuQuery[0]
        orderSku.status = '200'
        orderSku.save()
        skuTotalPrice = float(orderSku.skuPrice) * int(orderSku.skuQuantity)
        order = orderSku.order
        order.priceTotal = float(order.priceTotal) - skuTotalPrice
        order.save()
        response_data = {}
        _order = {}
        _order['orderId'] = order.id
        _order['priceTotal'] = float(order.priceTotal)
        _order['status'] = order.status
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')
        response_data['orderInfo'] = _order

        _sku = {}
        _sku['orderSkuId'] = orderSku.id
        _sku['skuId'] = orderSku.skuId
        _sku['skuName'] = orderSku.skuName.encode('utf-8')
        _sku['skuPrice'] = float(orderSku.skuPrice)
        _sku['skuSizeName'] = str(orderSku.skuSizeName)
        _sku['skuQuantity'] = float(orderSku.skuQuantity)
        _sku['skuStatus'] = orderSku.status
        response_data['orderSkuInfo'] = _sku

        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def waiterFinishOrder(request):
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
        waiter = Waiter.objects.select_related().get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _orderId = request.REQUEST.get('orderId')
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    try:
        order = Order.objects.get(id = _orderId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取餐桌信息失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if order.status == '0' and str(order.waiterId) == str(_waiterId):
        if order.userId == '':
            orderSkuQuery = order.ordersku_set.all().order_by('-id')
            logger.info(orderSkuQuery)
            orderSkuQuery = orderSkuQuery.exclude(status = '10').exclude(status = '200')
            logger.info(orderSkuQuery)
            if len(orderSkuQuery) != 0:
                response['code'] = -1
                response['errorMsg'] = '有未处理菜品'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

            order.status = '4'
            order.save()
            submitRecord = u'就餐完毕'.encode('utf-8')
            record = OrderRecord(record = submitRecord,order=order,date = datetime.datetime.now())
            record.save()

            try:
                table = Table.objects.get(id = str(order.tableId))
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取餐桌信息失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            table.status = '0'
            table.save()
            response_data = {}
            _table = {}
            _table['tableId'] = table.id
            _table['tableNumber'] = table.number.encode('utf-8')
            _table['tablePeopleNumber'] = table.peopleNumber
            _table['tableStatus'] = table.status
            response_data['tableInfo']=(_table)
            _order = {}
            _order['orderId'] = order.id
            _order['priceTotal'] = float(order.priceTotal)
            _order['status'] = order.status
            shanghai_tz = pytz.timezone('Asia/Shanghai')
            _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')
            response_data['orderInfo'] = _order
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            order.status = '4'
            order.save()
            try:
                user = User.objects.get(id = str(order.userId))
            except ObjectDoesNotExist:
                logger.info('不存在')
                response['code'] = 0
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            else:
                _deviceInfo = user.deviceInfo
                if(len(_deviceInfo and "iOS") == 3):
                    pushRst = pushAPNToUser(user.deviceToken,'0',str(order.id))
                elif(len(_deviceInfo and 'Android') == 7):
                    pushRst = pushMessageToSingle(user.clientID,'0',str(order.id))
                response['code'] = 0
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '无权操作'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def waiterGetShopDoingOrderList(request):
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

    _orderId = request.REQUEST.get('orderId')
    _limit = request.REQUEST.get('limit',20)
    _limit = int(_limit)
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _orderId = str(_orderId)
    if _orderId == '0':
        orderQuery = Order.objects.filter(waiterId =str(waiter.id)).filter(Q(status = '0') | Q (status = '4') )
    else:
        orderQuery = Order.objects.filter(waiterId =str(waiter.id)).filter(Q(status = '0') | Q (status = '4')).filter(id__lt = _orderId)
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
        orderList.append(_order)
    response['code'] = 0
    response['data'] = orderList
    return HttpResponse(json.dumps(response),content_type = "application/json")


@csrf_exempt
def waiterGetShopOrderDetail(request):
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
    _order['orderId'] = order.id
    _order['priceTotal'] = float(order.priceTotal)
    _order['status'] = order.status
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')

    _tableInfo = {}
    _tableInfo['tableId'] = order.id
    _tableInfo['tableNumber'] = order.tableNumber
    _order['tableInfo'] = _tableInfo

    _waiter_Info = {}
    _waiter_Info['waiterId'] = str(order.waiterId)
    _waiter_Info['waiterName'] = str(order.waiterName)
    _order['waiterInfo'] = _waiter_Info

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
    orderSkuQuery = OrderSku.objects.filter(order__id = order.id)
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
    response['data'] = _order
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type = "application/json")


@csrf_exempt
def waiterGetShopOrderDetailWithTable(request):
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

    _tableId = request.REQUEST.get('tableId')
    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _tableId = str(_tableId)
    try:
        order = Order.objects.filter(tableId =_tableId).filter(Q(status = '0') | Q (status = '2')).last()
    except IndexError:
        response['code'] = -1
        response['errorMsg'] = '获取订单失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _order = {}
    _order['orderId'] = str(order.id)
    _order['tableId'] = str(order.tableId)
    _order['tableNumber'] = str(order.tableNumber)
    _order['priceTotal'] = float(order.priceTotal)
    _order['status'] = order.status
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')

    _waiter_Info = {}
    _waiter_Info['waiterId'] = str(order.waiterId)
    _waiter_Info['waiterName'] = str(order.waiterName)
    _order['waiterInfo'] = _waiter_Info

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
    orderSkuQuery = OrderSku.objects.filter(order__id = order.id)
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
    response['data'] = _order
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type = "application/json")

@csrf_exempt
def waiterGetShopOrderListWithTable(request):
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

    _tableId = request.REQUEST.get('tableId')
    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _orderId = request.REQUEST.get('orderId')
    if _orderId == None or _orderId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderId失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _limit = request.REQUEST.get('limit',20)
    _limit = int(_limit)
    _tableId = str(_tableId)
    _orderId = str(_orderId)

    if _orderId == '0':
        orderQuery = Order.objects.filter(waiterId =str(waiter.id)).filter(tableId = _tableId)
    else:
        orderQuery = Order.objects.filter(waiterId =str(waiter.id)).filter(id__lt = _orderId).filter(tableId = _tableId)
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
        orderList.append(_order)
    response['code'] = 0
    response['data'] = orderList
    return HttpResponse(json.dumps(response),content_type = "application/json")
