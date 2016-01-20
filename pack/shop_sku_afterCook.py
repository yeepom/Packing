#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Category,AfterCook
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')


@csrf_exempt
def addAfterCooksToCategory(request):
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
    _afterCookList = request.REQUEST.getlist('afterCookList[]')
    if _afterCookList == []:
        response['code'] = -1
        response['errorMsg'] = '获取后打荷列表失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取类别失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if category.categoryType == '0':

        response_afterCookList = []
        for _afterCookId in _afterCookList:
            _afterCookId = str(_afterCookId)
            try:
                afterCook = AfterCook.objects.get(id = _afterCookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取后打荷失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if afterCook.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '后打荷'+afterCook.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if afterCook.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif afterCook.category == None:
                afterCook.category = category
                afterCook.save()
                _afterCook = {}
                _afterCook['afterCookId'] = afterCook.id
                _afterCook['afterCookName'] = afterCook.name
                _afterCook['afterCookTelephone'] = afterCook.telephone
                _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
                response_afterCookList.append(_afterCook)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_afterCookList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '1':
        response_afterCookList = []
        for _afterCookId in _afterCookList:
            _afterCookId = str(_afterCookId)
            try:
                afterCook = AfterCook.objects.get(id = _afterCookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取后打荷失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if afterCook.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '后打荷'+afterCook.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if afterCook.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif afterCook.category == None:
                afterCook.category = category
                afterCook.save()
                _afterCook = {}
                _afterCook['afterCookId'] = afterCook.id
                _afterCook['afterCookName'] = afterCook.name
                _afterCook['afterCookTelephone'] = afterCook.telephone
                _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
                response_afterCookList.append(_afterCook)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_afterCookList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该品类无需添加后打荷'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeAfterCookInCategory(request):
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
    _afterCookId = request.REQUEST.get('afterCookId')
    if _afterCookId == None or _afterCookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取后打荷id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    _afterCookId = str(_afterCookId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    afterCookCount = category.aftercook_set.count()
    if category.categoryType == '0' and afterCookCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个后打荷'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '1' and afterCookCount <= 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个后打荷'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '0' and afterCookCount >1:
        try:
            afterCook = AfterCook.objects.get(id = _afterCookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取后打荷失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(afterCook.category.id) == _categoryId:
            afterCook.category = None
            afterCook.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '该账号未关联'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif category.categoryType == '1' and afterCookCount >1:
        try:
            afterCook = AfterCook.objects.get(id = _afterCookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取后打荷失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if str(afterCook.category.id) == _categoryId:
            afterCook.category = None
            afterCook.save()
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
def getAfterCooksInCategory(request):
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
    afterCookList = category.aftercook_set.all()

    _afterCookList = []
    for afterCook in afterCookList:
        _afterCook = {}
        _afterCook['afterCookId'] = afterCook.id
        _afterCook['afterCookName'] = afterCook.name
        _afterCook['afterCookTelephone'] = afterCook.telephone
        _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
        _afterCookList.append(_afterCook)
    response['code'] = 0
    response['data'] = _afterCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def getFreeAfterCookList(request):
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
    afterCookQuery = AfterCook.objects.filter(shopId = str(_shopId)).filter(category = None)

    _afterCookList = []
    for afterCook in afterCookQuery:
        _afterCook = {}
        _afterCook['afterCookId'] = afterCook.id
        _afterCook['afterCookName'] = afterCook.name
        _afterCook['afterCookTelephone'] = afterCook.telephone
        _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
        _afterCookList.append(_afterCook)
    response['code'] = 0
    response['data'] = _afterCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

