__author__ = 'mike'
#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Cook,OrderSkuBackup
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist
from pack.tasks import cookSyncOrderSku
import pytz

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def cookGetCurrentOrderSkuBackupList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
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

    dispatchUnit = cook.category.dispatchUnit
    orderSkuBackupQuery = OrderSkuBackup.objects.filter(categoryId = str(cook.category.id))
    orderSkuBackupDispatchedQuery = orderSkuBackupQuery.filter(status = '2').filter(cookId = str(cook.id))
    orderSkuBackupDispatchedQueryCount = orderSkuBackupDispatchedQuery.count()
    print dispatchUnit
    print orderSkuBackupDispatchedQueryCount
    print type(dispatchUnit)
    print type(orderSkuBackupDispatchedQueryCount)
    if orderSkuBackupDispatchedQueryCount > dispatchUnit:
        orderSkuBackupDispatchedQuery = orderSkuBackupDispatchedQuery[:dispatchUnit]
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
            orderSkuBackupList.append(_orderSkuBackup)
        response['code'] = 0
        response['data'] = orderSkuBackupList
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif orderSkuBackupDispatchedQueryCount == dispatchUnit:
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
            orderSkuBackupList.append(_orderSkuBackup)
        response['code'] = 0
        response['data'] = orderSkuBackupList
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif orderSkuBackupDispatchedQueryCount < dispatchUnit:
        orderSkuBackupDispatchingQuery = orderSkuBackupQuery.filter(status='0')[:dispatchUnit-orderSkuBackupDispatchedQueryCount]
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
                orderSkuBackupList.append(_orderSkuBackup)
            response['code'] = 0
            response['data'] = orderSkuBackupList
            return HttpResponse(json.dumps(response),content_type="application/json")
        orderSkuBackupId = []
        for orderSkuBackup in orderSkuBackupDispatchingQuery:
            orderSkuBackupId.append(int(orderSkuBackup.id))

        rst = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId).update(status='2',cookId=str(cook.id),cookName = str(cook.name))
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
                orderSkuBackupList.append(_orderSkuBackup)
            orderSkuListDispatching = []
            for orderSkuBackupDispatching in orderSkuBackupDispatchingQuery:
                orderSkuListDispatching.append(int(orderSkuBackupDispatching.orderSkuId))
            cookSyncOrderSku.delay(str(cook.id),str(cook.name),'2',orderSkuListDispatching)
            response['code'] = 0
            response['data'] = orderSkuBackupList
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            response['code'] = 0
            return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def cookFinishOrderSkuBackupList(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
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
        cook = Cook.objects.get(id = _cookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != cook.lastLoginTime:
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

        if orderSkuBackup.status == '2' and orderSkuBackup.cookId == str(cook.id):
            orderSkuBackup.status = '4'
            orderSkuBackup.save()
        else:
            response['code'] = -1
            response['errorMsg'] = 'orderSku状态错误'
            return HttpResponse(json.dumps(response),content_type="application/json")
        orderSkuListDispatching.append(int(orderSkuBackup.orderSkuId))
    cookSyncOrderSku.delay(str(cook.id),str(cook.name),'4',orderSkuListDispatching)
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")

    # count = len(_orderSkuBackupList)
    # print 'count'
    # print count
    # orderSkuBackupQuery = OrderSkuBackup.objects.filter(categoryId = str(cook.category.id)).filter(status='0')[:count]
    # orderSkuBackupId = []
    # for orderSkuBackup in orderSkuBackupQuery:
    #     orderSkuBackupId.append(int(orderSkuBackup.id))
    # print orderSkuBackupQuery
    # rst = OrderSkuBackup.objects.filter(pk__in = orderSkuBackupId).update(status='2',cookId=str(cook.id),cookName = str(cook.name))
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
    #         _orderSkuBackup['skuSizeStatus'] = '2'
    #         orderSkuBackupList.append(_orderSkuBackup)
    #         orderSkuListDispatching.append(int(orderSkuBackup.orderSkuId))
    #     cookSyncOrderSku.delay(str(cook.id),str(cook.name),'2',orderSkuListDispatching)
    #     response['code'] = 0
    #     response['data'] = orderSkuBackupList
    #     return HttpResponse(json.dumps(response),content_type="application/json")
    # else:
    #     response['code'] = 0
    #     return HttpResponse(json.dumps(response),content_type="application/json")


