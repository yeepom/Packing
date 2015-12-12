#encoding:utf-8
from django.http import HttpResponse
import sys,json,re,logging,datetime
from pack.models import Shop,Table,Order
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def getTableList(request):
    logger = logging.getLogger('Pack.app')
    logger.info(request.REQUEST)
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    response_data = {}
    _shopId = request.session.get('shopId')
    _shopId = str(_shopId)
    if not _shopId:
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
        shop = Shop.objects.select_related().get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != shop.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    tableQuery = Table.objects.filter(shop = shop).filter(isValid = True).order_by('-id')

    response_data_tables = []
    for table in tableQuery:
        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number.encode('utf-8')
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        response_data_tables.append(_table)
    response_data['tables'] = response_data_tables
    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def tableInfo(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
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

    _method = request.REQUEST.get('method')
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = '获取method失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _method = str(_method)

    #if method = 0 , add;  method = 2 , queryOne; method = 3, delete
    if _method == '0':
        _tableNumber = request.REQUEST.get('tableNumber')
        if _tableNumber == None or _tableNumber == '':
            response['code'] = -1
            response['errorMsg'] = '请输入餐桌号'
            return HttpResponse(json.dumps(response),content_type="application/json")
        _peopleNumber = request.REQUEST.get('tablePeopleNumber')
        if _peopleNumber == None or _peopleNumber == '':
            response['code'] = -1
            response['errorMsg'] = '请输入最大容纳人数'
            return HttpResponse(json.dumps(response),content_type="application/json")

        _tableNumber = str(_tableNumber)
        _peopleNumber = int(_peopleNumber)
        table = Table(shop = shop, number = _tableNumber, peopleNumber= _peopleNumber,lockDateTime =
        datetime.datetime.now())
        table.save()
        response['code'] = 0
        response_data = {}
        response_data['tableNumber'] = table.number
        response_data['tablePeopleNumber'] = table.peopleNumber
        response_data['tableStatus'] = table.status
        response_data['tableId'] = table.id
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '2':
        _tableId = request.REQUEST.get('tableId')
        if _tableId == None or _tableId == '':
            response['code'] = -1
            response['errorMsg'] = '请输入tableid'
            return HttpResponse(json.dumps(response),content_type="application/json")

        try:
            table = Table.objects.get(id = _tableId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = 'table查询失败'
            return HttpResponse(json.dumps(response),content_type="application/json")

        response['code'] = 0
        response_data = {}
        response_data['tableNumber'] = table.number
        response_data['tablePeopleNumber'] = table.peopleNumber
        response_data['tableStatus'] = table.status
        response_data['tableId'] = table.id
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '3':
        _tableId = request.REQUEST.get('tableId')
        if _tableId == None or _tableId == '':
            response['code'] = -1
            response['errorMsg'] = '请输入tableid'
            return HttpResponse(json.dumps(response),content_type="application/json")
        try:
            table = Table.objects.get(id = _tableId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = 'table查询失败'
            return HttpResponse(json.dumps(response),content_type="application/json")

        table.isValid = False
        table.save()
        response['code'] = 0
        response['data'] = {}
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def alterTableNumber(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
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
    _tableNumber = request.REQUEST.get('tableNumber')

    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入tableid'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _tableNumber == None or _tableNumber == '':
        response['code'] = -1
        response['errorMsg'] = '请输入餐桌号'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _tableNumber = str(_tableNumber)

    try:
        table = Table.objects.get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = 'table查询失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    table.number = _tableNumber
    table.save()

    response['code'] = 0
    response_data = {}
    response_data['tableNumber'] = table.number
    response_data['tablePeopleNumber'] = table.peopleNumber
    response_data['tableStatus'] = table.status
    response_data['tableId'] = table.id
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterTablePeopleNumber(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
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
    _peopleNumber = request.REQUEST.get('tablePeopleNumber')

    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入tableId'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if _peopleNumber == None or _peopleNumber == '':
        response['code'] = -1
        response['errorMsg'] = '请输入容纳人数'
        return HttpResponse(json.dumps(response),content_type="application/json")

    _peopleNumber = str(_peopleNumber)

    try:
        table = Table.objects.get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = 'table查询失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    table.peopleNumber = _peopleNumber
    table.save()

    response['code'] = 0
    response_data = {}
    response_data['tableNumber'] = table.number
    response_data['tablePeopleNumber'] = table.peopleNumber
    response_data['tableStatus'] = table.status
    response_data['tableId'] = table.id
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def resetTableStatus(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
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

    if _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '请输入tableId'
        return HttpResponse(json.dumps(response),content_type="application/json")


    try:
        table = Table.objects.get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = 'table查询失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    if table.status == '0':
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif table.status == '2' or table.status ==  '1':
        table.status = '0'
        table.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif table.status == '3':
        orderQuery = Order.objects.filter(tableId = str(table.id)).filter(status = '0')
        if orderQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该餐桌有未完成订单'
            return HttpResponse(json.dumps(response),content_type="application/json")
        table.status='0'
        table.save()

        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
