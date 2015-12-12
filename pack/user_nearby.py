#encoding:utf-8
from django.http import HttpResponse
import sys,json,time,datetime
from pack.models import User,Shop,Table,Order
from django.contrib.gis import geos
from django.contrib.gis import measure
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import logging
from django.core.cache import cache
from django.core.paginator import Paginator,EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def getShopsNearby(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response_data = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ###################END#################

    _longitude = request.REQUEST.get('longitude')
    _latitude = request.REQUEST.get('latitude')

    if _longitude == None or _latitude == None:
        response['code'] = -1
        response['errorMsg'] = '定位失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _longitude == '' or _latitude == '':
        response['code'] = -1
        response['errorMsg'] = '定位失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _page = request.REQUEST.get('page',0)
    _page = int(_page)
    _limit = request.REQUEST.get('limit',20)
    _limit = int(_limit)
    if _page == None or _page == '':
        response['code'] = -1
        response['errorMsg'] = '获取页数失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    current_point = geos.fromstr("POINT(%s %s)" % (_longitude, _latitude))
    distance_from_point = {'km': 1000}
    shopsQuery = Shop.gis.filter(location__distance_lte=(current_point, measure.D(**distance_from_point)))
    shopsQuery = shopsQuery.distance(current_point).filter(isServiceOn = True).order_by('distance').annotate(
        tables=Count('table'))

    shopsPage = Paginator(shopsQuery, _limit)
    pageNums = shopsPage.num_pages
    try:
        shops = shopsPage.page(_page+1)
    except EmptyPage:
        shops = []
    response_data['more_exist'] = '0'
    if pageNums > _page+1:
        response_data['more_exist'] = '1'

    listOfShopsNearby = []
    cursor = 0
    for shop in shops:
        _shop = {}
        _shop['shopId'] = shop.id
        _shop['shopName'] = shop.name
        _shop['shopTelephone'] = shop.telephone
        print shop.tables
        # print shop.table_set().all()
        # _shop['tableNumber'] = shop.table_set().count()
        _shop['shopType'] = shop.shopType
        _headImage = shop.headImage+'!100'
        _shop['shopHeadImage'] = _headImage
        _distance = shop.distance.m
        _distance = int(_distance)
        if _distance < 1000:
            __distance = str(_distance)+"m"     #123m
        elif _distance > 1000 and _distance < 1000*1000:
            _distance_below_kilometer = int(_distance % 1000)
            logger.info(_distance_below_kilometer)
            if _distance_below_kilometer == 0:
                _distance = int(_distance / 1000)
                __distance = str(_distance)+"km"    #1km
            else:
                _distance_below_kilometer =  (_distance_below_kilometer / 10)
                _distance = int(_distance / 1000)
                __distance = str(_distance)+"."+str(_distance_below_kilometer)+"km"    #1.23km

        _shop['distance'] = __distance
        _shop['longitude'] = shop.location.x
        _shop['latitude'] = shop.location.y
        if cursor < _limit:
            listOfShopsNearby.append(_shop)
        cursor = cursor + 1
    response_data['shops'] = listOfShopsNearby
    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def getTablesWithShop(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _shopId = request.REQUEST.get('shopId')

    if _shopId == None or _shopId == '':
        response['code'] = -1
        response['errorMsg'] = '获取商家id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    try:
        shop = Shop.objects.select_related().get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '获取商家信息失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    tables = shop.table_set.filter(isValid = True).filter(status = '0')
    _tables = []
    for table in tables:
        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number
        _table['tablePeopleNumber'] = table.peopleNumber
        _tables.append(_table)
    response['code'] = 0
    response['data'] = _tables
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def userLockTable(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response_data = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################
    _tableId = request.REQUEST.get('tableId')
    if  _tableId == None or _tableId == '':
        response['code'] = -1
        response['errorMsg'] = '获取餐桌id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _tableId = str(_tableId)
    tableLockQuery = TableLock.objects.select_related().filter(user = user).filter(table__status = '1').filter(
        table__isValid = True)
    _tableLockQuery = tableLockQuery.filter(table__id = _tableId)
    if _tableLockQuery.exists():
        response['code'] = -1
        response['errorMsg'] = '您已经锁定了该餐桌'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if tableLockQuery.exists():
        response['code'] = -1
        response['errorMsg'] = '锁定失败，您锁定了其他餐桌'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    try:
        table = Table.objects.get(id = _tableId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取table失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    logger.info(table.status)
    if str(table.status) == '0':
        table.status = '1'
        table.save()
        tableLock  = TableLock(table = table,user = user, date = datetime.datetime.now())
        tableLock.save()
#        checkTableStatusTask.delay(lockTimeStamp,_userId,_tableId)
        response['code'] = 0
        response['data'] = {'tableLockId':str(tableLock.id)}
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif str(table.status) == '1':
        response['code'] = 0
        response['data'] = {'tableLockId':str(_tableLockQuery[0].id)}
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif str(table.status) == '2' or str(table.status) == '3':
        response['code'] = -1
        response['errorMsg'] = '该餐桌已经有人预定'
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif str(table.status) == '200':
        response['code'] = -1
        response['errorMsg'] = '该餐桌暂不对外开放'
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def userUnlockTable(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################
    _tableLockId = request.REQUEST.get('tableLockId')
    if  _tableLockId == None or _tableLockId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableLockId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    try:
        tableLock = TableLock.objects.select_related().get(id = _tableLockId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取tableLock失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    table = tableLock.table
    if table.status == '1' and tableLock.user == user and tableLock.isValid == True :
        table.status = '0'
        table.save()
        tableLock.isValid = False
        tableLock.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def userGetTableLockDetail(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response_data = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################
    _tableLockId = request.REQUEST.get('tableLockId')
    if  _tableLockId == None or _tableLockId == '':
        response['code'] = -1
        response['errorMsg'] = '获取tableLockId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    try:
        tableLock = TableLock.objects.select_related().get(id = _tableLockId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取tableLock失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    table = tableLock.table
    _table = {}
    _table['tableId'] = table.id
    _table['tableNumber'] = table.number
    _table['tablePeopleNumber'] = table.peopleNumber
    _table['tableStatus'] = table.status
    response_data['tableInfo'] = _table
    _shop = {}
    _shop['shopId'] = table.shop.id
    _shop['shopName'] = table.shop.name
    response_data['shopInfo'] = _shop
    if table.status == '1':
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif table.status == '2':
        try:
            order = Order.objects.filter(userId = str(_userId)).filter(Q(status = '0') | Q (status = '1')).first()
        except IndexError:
            logger.info('获取正在忙碌的order失败')
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        _order = {}
        _order['orderId'] = order.id
        _order['priceTotal'] = float(order.pricetotal)
        response_data['orderInfo'] = _order
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def checkUserTable(request):
    logger = logging.getLogger('Pack.app')
    logger.info('----------------------------')
    response = {}
    response_data = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    tableLockQuery = TableLock.objects.select_related().filter(user = user).filter(Q(table__status = '1')|Q(
        table__status = '2')).filter(table__isValid = True)
    if not tableLockQuery.exists():
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        table = tableLockQuery[0].table
        _table = {}
        _table['tableId'] = table.id
        _table['tableNumber'] = table.number
        _table['tablePeopleNumber'] = table.peopleNumber
        _table['tableStatus'] = table.status
        response_data['tableInfo'] = _table
        _shop = {}
        _shop['shopId'] = table.shop.id
        _shop['shopName'] = table.shop.name
        response_data['shopInfo'] = _shop
        if table.status == '1':
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")
        elif table.status == '2':
            try:
                order = Order.objects.filter(userId = str(_userId)).filter(Q(status = '0') | Q (status = '1')).first()
            except IndexError:
                logger.info('获取正在忙碌的order失败')
                response['code'] = 0
                response['data'] = response_data
                return HttpResponse(json.dumps(response),content_type="application/json")
            _order = {}
            _order['orderId'] = order.id
            _order['priceTotal'] = float(order.pricetotal)
            response_data['orderInfo'] = _order
            response['code'] = 0
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def getShopDetail(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    response_data = {}
    _shopId = request.REQUEST.get('shopId')
    if _shopId == None or _shopId == '':
        response['code'] = -1
        response['errorMsg'] = '获取商家信息失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    try:
        shop = Shop.objects.get(id = _shopId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    response_data['shopName'] = shop.name
    response_data['shopTelephone'] = shop.telephone
    response_data['shopHeadImage'] = shop.headImage
    response_data['longitude'] = shop.location.x
    response_data['latitude'] = shop.location.y
    response_data['province'] = shop.province
    response_data['city'] = shop.city
    response_data['district'] = shop.district
    response_data['addressDetail'] = shop.addressDetail
    response_data['startTimeStamp'] = str(shop.startTimeStamp)
    response_data['endTimeStamp'] = str(shop.endTimeStamp)
    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")

