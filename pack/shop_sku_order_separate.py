#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Category,OrderSeparate
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def addOrderSeparatesToCategory(request):
    logger = logging.getLogger('Pack.app')
    logger.info(request)
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

    _categoryId = request.REQUEST.get('categoryId')
    if _categoryId == None or _categoryId == '':
        response['code'] = -1
        response['errorMsg'] = '获取类别id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _orderSeparateList = request.REQUEST.getlist('orderSeparateList[]')
    if _orderSeparateList == []:
        response['code'] = -1
        response['errorMsg'] = '获取配菜列表失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取类别失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if category.categoryType == '0' or category.categoryType == '1' or category.categoryType == '2':

        response_orderSeparateList = []
        for _orderSeparateId in _orderSeparateList:
            _orderSeparateId = str(_orderSeparateId)
            try:
                orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取配菜失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if orderSeparate.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '配菜'+orderSeparate.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if orderSeparate.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif orderSeparate.category == None:
                orderSeparate.category = category
                orderSeparate.save()
                _orderSeparate = {}
                _orderSeparate['orderSeparateId'] = orderSeparate.id
                _orderSeparate['orderSeparateName'] = orderSeparate.name
                _orderSeparate['orderSeparateTelephone'] = orderSeparate.telephone
                _orderSeparate['everAttachCategory'] = '1' if orderSeparate.category != None else '0'
                response_orderSeparateList.append(_orderSeparate)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_orderSeparateList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该品类无需添加配菜'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeOrderSeparateInCategory(request):
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

    _categoryId = request.REQUEST.get('categoryId')
    if _categoryId == None or _categoryId == '':
        response['code'] = -1
        response['errorMsg'] = '获取categoryId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _orderSeparateId = request.REQUEST.get('orderSeparateId')
    if _orderSeparateId == None or _orderSeparateId == '':
        response['code'] = -1
        response['errorMsg'] = '获取配菜id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    _orderSeparateId = str(_orderSeparateId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    orderSeparateCount = category.orderseparate_set.count()
    if category.categoryType == '0' and orderSeparateCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个配菜'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '1' and orderSeparateCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个配菜'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '2' and orderSeparateCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个配菜'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '0' and orderSeparateCount >1:
        try:
            orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取配菜失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(orderSeparate.category.id) == _categoryId:
            orderSeparate.category = None
            orderSeparate.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '该账号未关联'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '1' and orderSeparateCount >1:
        try:
            orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取配菜失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(orderSeparate.category.id) == _categoryId:
            orderSeparate.category = None
            orderSeparate.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '该账号未关联'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '2' and orderSeparateCount >1:
        try:
            orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取配菜失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(orderSeparate.category.id) == _categoryId:
            orderSeparate.category = None
            orderSeparate.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '该账号未关联'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '您无法执行该操作'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def getOrderSeparatesInCategory(request):
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
    _categoryId =request.REQUEST.get('categoryId')
    if _categoryId == None or _categoryId == '':
        response['code'] = -1
        response['errorMsg'] = '获取品类id失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    _categoryId = str(_categoryId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    orderSeparateList = category.orderseparate_set.all()

    _orderSeparateList = []
    for orderSeparate in orderSeparateList:
        _orderSeparate = {}
        _orderSeparate['orderSeparateId'] = orderSeparate.id
        _orderSeparate['orderSeparateName'] = orderSeparate.name
        _orderSeparate['orderSeparateTelephone'] = orderSeparate.telephone
        _orderSeparate['everAttachCategory'] = '1' if orderSeparate.category != None else '0'
        _orderSeparateList.append(_orderSeparate)
    response['code'] = 0
    response['data'] = _orderSeparateList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def getFreeOrderSeparateList(request):
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
    orderSeparateQuery = OrderSeparate.objects.filter(shopId = str(_shopId)).filter(category = None)

    _orderSeparateList = []
    for orderSeparate in orderSeparateQuery:
        _orderSeparate = {}
        _orderSeparate['orderSeparateId'] = orderSeparate.id
        _orderSeparate['orderSeparateName'] = orderSeparate.name
        _orderSeparate['orderSeparateTelephone'] = orderSeparate.telephone
        _orderSeparate['everAttachCategory'] = '1' if orderSeparate.category != None else '0'
        _orderSeparateList.append(_orderSeparate)
    response['code'] = 0
    response['data'] = _orderSeparateList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

