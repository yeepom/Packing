__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Serve,OrderSku,Order,User,OrderSkuBackup,Shop
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from pack.tasks import serveSyncOrderSku

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def serveGetCurrentOrderSkuBackupList(request):
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

    if serve.shopId =='':
        response['code'] = 2
        response['errorMsg'] = '请先与店铺管理者绑定'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    try:
        shop = Shop.objects.get(id = str(serve.shopId))
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '查找shop失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    serveDispatchUnit = shop.serveDispatchUnit
    orderSkuBackupQuery = OrderSkuBackup.objects.filter(Q(status = '4') | Q(status = '5'))
    orderSkuBackupDispatchedQuery = orderSkuBackupQuery.filter(status = '5').filter(serveId = str(serve.id))
    orderSkuBackupDispatchedQueryCount = orderSkuBackupDispatchedQuery.count()
    if orderSkuBackupDispatchedQueryCount > serveDispatchUnit:
        orderSkuBackupDispatchedQuery = orderSkuBackupDispatchedQuery[:serveDispatchUnit]
        orderSkuBackupList = []
        for orderSkuBackup in orderSkuBackupDispatchedQuery:
            _orderSkuBackup = {}
            _orderSkuBackup['orderSkuBackupId'] = orderSkuBackup.id
            _orderSkuBackup['skuId'] = orderSkuBackup.skuId
            _orderSkuBackup['skuName'] = orderSkuBackup.skuName
            _orderSkuBackup['skuPrice'] = float(orderSkuBackup.skuPrice)
            _orderSkuBackup['skuSizeName'] = orderSkuBackup.skuSizeName
            _orderSkuBackup['skuQuantity'] = orderSkuBackup.skuQuantity
            _orderSkuBackup['skuSizeStatus'] = orderSkuBackup.status
            _orderSkuBackup['tableId'] = orderSkuBackup.tableId
            _orderSkuBackup['tableNumber'] = orderSkuBackup.tableNumber
            _orderSkuBackup['cookName'] = orderSkuBackup.cookName
            orderSkuBackupList.append(_orderSkuBackup)
        response['code'] = 0
        response['data'] = orderSkuBackupList
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif orderSkuBackupDispatchedQueryCount == serveDispatchUnit:
        orderSkuBackupList = []
        for orderSkuBackup in orderSkuBackupDispatchedQuery:
            _orderSkuBackup = {}
            _orderSkuBackup['orderSkuBackupId'] = orderSkuBackup.id
            _orderSkuBackup['skuId'] = orderSkuBackup.skuId
            _orderSkuBackup['skuName'] = orderSkuBackup.skuName
            _orderSkuBackup['skuPrice'] = float(orderSkuBackup.skuPrice)
            _orderSkuBackup['skuSizeName'] = orderSkuBackup.skuSizeName
            _orderSkuBackup['skuQuantity'] = orderSkuBackup.skuQuantity
            _orderSkuBackup['skuSizeStatus'] = orderSkuBackup.status
            _orderSkuBackup['tableId'] = orderSkuBackup.tableId
            _orderSkuBackup['tableNumber'] = orderSkuBackup.tableNumber
            _orderSkuBackup['cookName'] = orderSkuBackup.cookName
            orderSkuBackupList.append(_orderSkuBackup)
        response['code'] = 0
        response['data'] = orderSkuBackupList
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif orderSkuBackupDispatchedQueryCount < serveDispatchUnit:
        orderSkuBackupDispatchingQuery = orderSkuBackupQuery.filter(status='4')[:serveDispatchUnit-orderSkuBackupDispatchedQueryCount]
        if not orderSkuBackupDispatchingQuery.exists():
            orderSkuBackupList = []
            for orderSkuBackup in orderSkuBackupDispatchedQuery:
                _orderSkuBackup = {}
                _orderSkuBackup['orderSkuBackupId'] = orderSkuBackup.id
                _orderSkuBackup['skuId'] = orderSkuBackup.skuId
                _orderSkuBackup['skuName'] = orderSkuBackup.skuName
                _orderSkuBackup['skuPrice'] = float(orderSkuBackup.skuPrice)
                _orderSkuBackup['skuSizeName'] = orderSkuBackup.skuSizeName
                _orderSkuBackup['skuQuantity'] = orderSkuBackup.skuQuantity
                _orderSkuBackup['skuSizeStatus'] = orderSkuBackup.status
                _orderSkuBackup['tableId'] = orderSkuBackup.tableId
                _orderSkuBackup['tableNumber'] = orderSkuBackup.tableNumber
                _orderSkuBackup['cookName'] = orderSkuBackup.cookName
                orderSkuBackupList.append(_orderSkuBackup)
            response['code'] = 0
            response['data'] = orderSkuBackupList
            return HttpResponse(json.dumps(response),content_type="application/json")
        orderSkuBackupId = []
        for orderSkuBackup in orderSkuBackupDispatchingQuery:
            orderSkuBackupId.append(int(orderSkuBackup.id))

        rst = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId).update(status='5',serveId=str(serve.id),serveName = str(serve.name))
        if rst == 1:
            orderSkuBackupDispatchedNewQuery = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId)
            orderSkuBackupAllQuery = orderSkuBackupDispatchedQuery | orderSkuBackupDispatchedNewQuery
            orderSkuBackupList = []
            for orderSkuBackup in orderSkuBackupAllQuery:
                _orderSkuBackup = {}
                _orderSkuBackup['orderSkuBackupId'] = orderSkuBackup.id
                _orderSkuBackup['skuId'] = orderSkuBackup.skuId
                _orderSkuBackup['skuName'] = orderSkuBackup.skuName
                _orderSkuBackup['skuPrice'] = float(orderSkuBackup.skuPrice)
                _orderSkuBackup['skuSizeName'] = orderSkuBackup.skuSizeName
                _orderSkuBackup['skuQuantity'] = orderSkuBackup.skuQuantity
                _orderSkuBackup['skuSizeStatus'] = orderSkuBackup.status
                _orderSkuBackup['tableId'] = orderSkuBackup.tableId
                _orderSkuBackup['tableNumber'] = orderSkuBackup.tableNumber
                _orderSkuBackup['cookName'] = orderSkuBackup.cookName
                orderSkuBackupList.append(_orderSkuBackup)
            orderSkuListDispatching = []
            for orderSkuBackupDispatching in orderSkuBackupDispatchingQuery:
                orderSkuListDispatching.append(int(orderSkuBackupDispatching.orderSkuId))
            serveSyncOrderSku.delay(str(serve.id),str(serve.name),'5',orderSkuListDispatching)
            response['code'] = 0
            response['data'] = orderSkuBackupList
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            response['code'] = 0
            return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def serveFinishOrderSkuBackupList(request):
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

    _orderSkuBackupList = request.REQUEST.getlist('orderSkuBackupList[]')

    if _orderSkuBackupList == None or _orderSkuBackupList == '':
        response['code'] = -1
        response['errorMsg'] = '请输入订单id'
        return HttpResponse(json.dumps(response),content_type="application/json")

    orderSkuListDispatching = []
    for _orderSkuBackupId in _orderSkuBackupList:
        _orderSkuBackupId = str(_orderSkuBackupId)
        try:
            orderSkuBackup = OrderSkuBackup.objects.get(id = _orderSkuBackupId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '查询orderSku失败'
            return HttpResponse(json.dumps(response),content_type="application/json")

        if orderSkuBackup.status == '5' and orderSkuBackup.serveId == str(serve.id):
            orderSkuBackup.status = '6'
            orderSkuBackup.save()
        else:
            response['code'] = -1
            response['errorMsg'] = 'orderSku状态错误'
            return HttpResponse(json.dumps(response),content_type="application/json")
        orderSkuListDispatching.append(int(orderSkuBackup.orderSkuId))
    serveSyncOrderSku.delay(str(serve.id),str(serve.name),'6',orderSkuListDispatching)
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")

    #add new ones
    # count = len(_orderSkuBackupList)
    # orderSkuBackupQuery = OrderSkuBackup.objects.filter(status='4')[:count]
    # orderSkuBackupId = []
    # for orderSkuBackup in orderSkuBackupQuery:
    #     orderSkuBackupId.append(int(orderSkuBackup.id))
    # rst = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId).update(status='5',serveId=str(serve.id),serveName = str(serve.name))
    # if rst == 1:
    #     orderSkuBackupNewQuery = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId)
    #     orderSkuBackupList = []
    #     orderSkuListDispatching = []
    #     for orderSkuBackup in orderSkuBackupNewQuery:
    #         _orderSkuBackup = {}
    #         _orderSkuBackup['orderSkuBackupId'] = orderSkuBackup.id
    #         _orderSkuBackup['skuId'] = orderSkuBackup.skuId
    #         _orderSkuBackup['skuName'] = orderSkuBackup.skuName
    #         _orderSkuBackup['skuPrice'] = float(orderSkuBackup.skuPrice)
    #         _orderSkuBackup['skuSizeName'] = orderSkuBackup.skuSizeName
    #         _orderSkuBackup['skuQuantity'] = orderSkuBackup.skuQuantity
    #         _orderSkuBackup['skuSizeStatus'] = orderSkuBackup.status
    #         _orderSkuBackup['tableId'] = orderSkuBackup.tableId
    #         _orderSkuBackup['tableNumber'] = orderSkuBackup.tableNumber
    #         _orderSkuBackup['cookName'] = orderSkuBackup.cookName
    #         orderSkuBackupList.append(_orderSkuBackup)
    #         orderSkuListDispatching.append(int(orderSkuBackup.orderSkuId))
    #     serveSyncOrderSku.delay(str(serve.id),str(serve.name),'5',orderSkuListDispatching)
    #
    #     response['code'] = 0
    #     response['data'] = orderSkuBackupList
    #     return HttpResponse(json.dumps(response),content_type="application/json")
    # else:
    #     response['code'] = 0
    #     return HttpResponse(json.dumps(response),content_type="application/json")
