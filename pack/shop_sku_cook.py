#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Category,Cook
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def addCooksToCategory(request):
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
        response['errorMsg'] = '获取categoryId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _cookList = request.REQUEST.getlist('cookList[]')
    if _cookList == None or _cookList == '':
        response['code'] = -1
        response['errorMsg'] = '获取cookList失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取类别失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if category.categoryType == '0':

        response_cookList = []
        for _cookId in _cookList:
            _cookId = str(_cookId)
            try:
                cook = Cook.objects.get(id = _cookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取厨师id失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if cook.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '厨师'+cook.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if cook.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif cook.category == None:
                cook.category = category
                cook.save()
                _cook = {}
                _cook['cookId'] = cook.id
                _cook['cookName'] = cook.name
                _cook['cookTelephone'] = cook.telephone
                response_cookList.append(_cook)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_cookList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该品类无需添加厨师'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeCookInCategory(request):
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
    _cookId = request.REQUEST.get('cookId')
    if _cookId == None or _cookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取厨师id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    _cookId = str(_cookId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    cookCount = category.cook_set.count()
    if category.categoryType == '0' and cookCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个厨师'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '0' and cookCount >1:
        try:
            cook = Cook.objects.get(id = _cookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取cook失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(cook.category.id) == _categoryId:
            cook.category = None
            cook.save()
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
def getCooksInCategory(request):
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
    cookList = category.cook_set.all()

    _cookList = []
    for cook in cookList:
        _cook = {}
        _cook['cookId'] = cook.id
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
        _cookList.append(_cook)
    response['code'] = 0
    response['data'] = _cookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def getFreeCookList(request):
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
    cookQuery = Cook.objects.filter(shopId = str(_shopId)).filter(category = None)

    _cookList = []
    for cook in cookQuery:
        _cook = {}
        _cook['cookId'] = cook.id
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
        _cookList.append(_cook)
    response['code'] = 0
    response['data'] = _cookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

