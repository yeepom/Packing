#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Category,BeforeCook
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def addBeforeCooksToCategory(request):
    logger = logging.getLogger('Pack.app')
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
    _beforeCookList = request.REQUEST.getlist('beforeCookList[]')
    logger.info(_beforeCookList)
    if _beforeCookList == []:
        response['code'] = -1
        response['errorMsg'] = '获取前打荷列表失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取类别失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if category.categoryType == '0':

        response_beforeCookList = []
        for _beforeCookId in _beforeCookList:
            _beforeCookId = str(_beforeCookId)
            try:
                beforeCook = BeforeCook.objects.get(id = _beforeCookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取前打荷失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if beforeCook.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '前打荷'+beforeCook.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if beforeCook.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif beforeCook.category == None:
                beforeCook.category = category
                beforeCook.save()
                _beforeCook = {}
                _beforeCook['beforeCookId'] = beforeCook.id
                _beforeCook['beforeCookName'] = beforeCook.name
                _beforeCook['beforeCookTelephone'] = beforeCook.telephone
                _beforeCook['everAttachCategory'] = '1' if beforeCook.category != None else '0'
                response_beforeCookList.append(_beforeCook)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_beforeCookList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该品类无需添加前打荷'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeBeforeCookInCategory(request):
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
    _beforeCookId = request.REQUEST.get('beforeCookId')
    if _beforeCookId == None or _beforeCookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取前打荷id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    _beforeCookId = str(_beforeCookId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    beforeCookCount = category.beforecook_set.count()
    if category.categoryType == '0' and beforeCookCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个前打荷'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '0' and beforeCookCount >1:
        try:
            beforeCook = BeforeCook.objects.get(id = _beforeCookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取前打荷失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(beforeCook.category.id) == _categoryId:
            beforeCook.category = None
            beforeCook.save()
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
def getBeforeCooksInCategory(request):
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
    beforeCookList = category.beforecook_set.all()

    _beforeCookList = []
    for beforeCook in beforeCookList:
        _beforeCook = {}
        _beforeCook['beforeCookId'] = beforeCook.id
        _beforeCook['beforeCookName'] = beforeCook.name
        _beforeCook['beforeCookTelephone'] = beforeCook.telephone
        _beforeCook['everAttachCategory'] = '1' if beforeCook.category != None else '0'
        _beforeCookList.append(_beforeCook)
    response['code'] = 0
    response['data'] = _beforeCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def getFreeBeforeCookList(request):
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
    beforeCookQuery = BeforeCook.objects.filter(shopId = str(_shopId)).filter(category = None)

    _beforeCookList = []
    for beforeCook in beforeCookQuery:
        _beforeCook = {}
        _beforeCook['beforeCookId'] = beforeCook.id
        _beforeCook['beforeCookName'] = beforeCook.name
        _beforeCook['beforeCookTelephone'] = beforeCook.telephone
        _beforeCook['everAttachCategory'] = '1' if beforeCook.category != None else '0'
        _beforeCookList.append(_beforeCook)
    response['code'] = 0
    response['data'] = _beforeCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

