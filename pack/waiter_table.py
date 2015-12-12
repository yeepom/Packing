#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Table,Waiter,Order,User,OrderSku
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import pytz

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def waiterGetTableList(request):
    response = {}
    response_data = {}
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
    if waiter.shop == None:
        response['code'] = 2
        response['errorMsg'] = '请联系管理员关联您的账户'
        return HttpResponse(json.dumps(response),content_type="application/json")

    tableQuery = Table.objects.filter(shop = waiter.shop).filter(isValid = True)
    response_data_tables = []
    for table in tableQuery:
        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number.encode('utf-8')
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        response_data_tables.append(_table)
    response['code'] = 0
    response['data'] = response_data_tables
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def waiterGetOwnTableList(request):
    response = {}
    response_data = {}
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
    if waiter.shop == None:
        response['code'] = 2
        response['errorMsg'] = '请联系管理员关联您的账户'
        return HttpResponse(json.dumps(response),content_type="application/json")

    tableQuery = Table.objects.filter(shop = waiter.shop).filter(isValid = True).filter(Q(status='2')|Q(
        status='3')).filter(waiterId = str(_waiterId))
    response_data_tables = []
    for table in tableQuery:
        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number.encode('utf-8')
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        response_data_tables.append(_table)
    response['code'] = 0
    response['data'] = response_data_tables
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def waiterGetTableDetail(request):
    response = {}
    response_data = {}
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
    if waiter.shop == None:
        response['code'] = 2
        response['errorMsg'] = '请联系管理员关联您的账户'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _tableId = request.REQUEST.get('tableId')
    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入tableid'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _tableId = str(_tableId)
    try:
        table = Table.objects.get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '查找table失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _table = {}
    _table['tableId'] = table.id
    _table['tableNumber'] = table.number.encode('utf-8')
    _table['tablePeopleNumber'] = table.peopleNumber
    _table['tableStatus'] = table.status
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    date = table.lockDateTime.astimezone(shanghai_tz)
    _table['lockDateTime'] = date.strftime('%Y/%m/%d %H:%M:%S')
    response_data['tableInfo'] = _table

    if table.status == '1':
        try:
            user = User.objects.filter(id = str(table.userId))
        except ObjectDoesNotExist:
            response_data['userInfo'] = ''
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        _table_lock_userInfo = {}
        _table_lock_userInfo['userId'] = str(user.id)
        _table_lock_userInfo['userTelephone'] = str(user.telephone)
        _table_lock_userInfo['userName'] = str(user.name)
        response_data['userInfo'] = _table_lock_userInfo
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif table.status == '2':
        try:
            waiter = Waiter.objects.get(id = str(table.waiterId))
        except ObjectDoesNotExist:
            response_data['waiterInfo'] = ''
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        _table_lock_waiter_order_Info = {}
        _table_lock_waiter_order_Info['waiterId'] = str(waiter.id)
        _table_lock_waiter_order_Info['waiterTelephone'] = str(waiter.telephone)
        _table_lock_waiter_order_Info['waiterName'] = str(waiter.name)
        _table_lock_waiter_order_Info['waiterHeadImage'] = str(waiter.headImage)
        response_data['waiterInfo'] = _table_lock_waiter_order_Info

        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif table.status == '3':
        orderQuery = Order.objects.select_related().filter(tableId =_tableId).filter(status = '0')
        if not orderQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '获取订单失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        order = orderQuery[0]
        _order = {}
        _order['orderId'] = str(order.id)
        _order['priceTotal'] = float(order.priceTotal)
        _order['status'] = order.status
        shanghai_tz = pytz.timezone('Asia/Shanghai')
        _order['dateTime'] = order.date.astimezone(shanghai_tz).strftime('%Y/%m/%d %H:%M:%S')
        _table = {}
        _table['tableId'] = str(order.tableId)
        _table['tableNumber'] = str(order.tableNumber)
        _order['tableInfo'] = _table
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

    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def setTableStatus(request):
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
    _method = request.REQUEST.get('method')
    _tableId = request.REQUEST.get('tableId')
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = '获取method失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入tableId'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _method = str(_method)
    _tableId = str(_tableId)

    try:
        table = Table.objects.get( id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '查找table失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    if  _method == '0':

        if table.status == '1':
            table.status = '0'
            table.userId = ''
            table.save()
            response['code'] = 0
            response_data = {}
            response_data['tableNumber'] = table.number
            response_data['tablePeopleNumber'] = table.peopleNumber
            response_data['tableStatus'] = table.status
            response_data['tableId'] = table.id
            response_data['waiterId'] = table.waiterId
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif  table.status == '2' and str(table.waiterId) == str(_waiterId):
            table.status = '0'
            table.waiterId = ''
            table.save()
            response['code'] = 0
            response_data = {}
            response_data['tableNumber'] = table.number
            response_data['tablePeopleNumber'] = table.peopleNumber
            response_data['tableStatus'] = table.status
            response_data['tableId'] = table.id
            response_data['waiterId'] = table.waiterId
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif table.status == '2' and str(table.waiterId) != str(_waiterId):
            response['code'] = -1
            response['errorMsg'] = '您没有权限'
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif table.status == '3':
            orderQuery = Order.objects.filter(tableId = _tableId).filter(Q(status = '0')|Q(
                status = '1')|Q(status = '2'))
            print orderQuery
            if len(orderQuery) > 0:
                response['code'] = -1
                response['errorMsg'] = '有订单未完成，暂无法设置为空闲'
                return HttpResponse(json.dumps(response),content_type="application/json")
            table.status = '0'
            table.save()
            response['code'] = 0
            response_data = {}
            response_data['tableNumber'] = table.number
            response_data['tablePeopleNumber'] = table.peopleNumber
            response_data['tableStatus'] = table.status
            response_data['waiterId'] = table.waiterId
            response_data['tableId'] = table.id
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        elif table.status == '0':
            response['code'] = -1
            response['errorMsg'] = '已经为空闲'
            return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '1':
        response['code'] = -1
        response['errorMsg'] = '您无权进行此操作'
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif  _method == '2':
        if table.status == '0' or table.status == '1':
            table.status = '2'
            table.waiterId = str(_waiterId)
            table.save()
            response['code'] = 0
            response_data = {}
            response_data['tableNumber'] = table.number
            response_data['tablePeopleNumber'] = table.peopleNumber
            response_data['tableStatus'] = table.status
            response_data['tableId'] = table.id
            try:
                waiter = Waiter.objects.get(id = str(_waiterId))
            except ObjectDoesNotExist:
                response_data['waiterInfo'] = ''
                response['code'] = 0
                response['data'] = response_data
                return HttpResponse(json.dumps(response),content_type="application/json")
            _table_lock_waiter_order_Info = {}
            _table_lock_waiter_order_Info['waiterId'] = str(waiter.id)
            _table_lock_waiter_order_Info['waiterTelephone'] = str(waiter.telephone)
            _table_lock_waiter_order_Info['waiterName'] = str(waiter.name)
            _table_lock_waiter_order_Info['waiterHeadImage'] = str(waiter.headImage)
            response_data['waiterInfo'] = _table_lock_waiter_order_Info

            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        elif table.status == '3':
            response['code'] = -1
            response['errorMsg'] = '您无权进行此操作'
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif table.status == '2':
            response['code'] = -1
            response['errorMsg'] = '已经为锁定'
            return HttpResponse(json.dumps(response),content_type="application/json")
    elif  _method == '3':
        if table.status == '0' or table.status == '1' or table.status == '2':
            response['code'] = -1
            response['errorMsg'] = '生成订单，餐桌会自动变为忙碌'
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif table.status == '3':
            response['code'] = 0
            response_data = {}
            response_data['tableNumber'] = table.number
            response_data['tablePeopleNumber'] = table.peopleNumber
            response_data['tableStatus'] = table.status
            response_data['tableId'] = table.id
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

    response['code'] = -1
    response['errorMsg'] = 'method错误'
    return HttpResponse(json.dumps(response),content_type="application/json")
