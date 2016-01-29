#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Category,Serve
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')



@csrf_exempt
def addServesToCategory(request):
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
    _serveList = request.REQUEST.getlist('serveList[]')
    if _serveList == []:
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
    if category.categoryType == '10' or category.categoryType == '11' or category.categoryType == '12':

        response_serveList = []
        for _serveId in _serveList:
            _serveId = str(_serveId)
            try:
                serve = Serve.objects.get(id = _serveId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取上菜员失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if serve.shopId != str(shop.id):
                response['code'] = -1
                response['errorMsg'] = '上菜员'+serve.name+'不在您的店铺下，您无权执行该操作'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if serve.category == category:
                response['code'] = -1
                response['errorMsg'] = '已经添加过啦'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            elif serve.category == None:
                serve.category = category
                serve.save()
                _serve = {}
                _serve['serveId'] = serve.id
                _serve['serveName'] = serve.name
                _serve['serveTelephone'] = serve.telephone
                _serve['everAttachCategory'] = '1' if serve.category != None else '0'
                response_serveList.append(_serve)
            else:
                response['code'] = -1
                response['errorMsg'] = '已经与其他类别关联'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        response['code'] = 0
        response['data'] = response_serveList
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该品类无需添加上菜员'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeServeInCategory(request):
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
    _serveId = request.REQUEST.get('serveId')
    if _serveId == None or _serveId == '':
        response['code'] = -1
        response['errorMsg'] = '获取上菜员id失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryId = str(_categoryId)
    _serveId = str(_serveId)
    try:
        category = Category.objects.get(id = _categoryId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取category失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    serveCount = category.serve_set.count()
    if category.categoryType == '10' or category.categoryType == '11' or category.categoryType == '12':
        if serveCount <= 1:
            response['code'] = -1
            response['errorMsg'] = '至少有一个上菜员'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        elif serveCount >1:
            try:
                serve = Serve.objects.get(id = _serveId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取配菜失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if str(serve.category.id) == _categoryId:
                serve.category = None
                serve.save()
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
def getServesInCategory(request):
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
    serveList = category.serve_set.all()

    _serveList = []
    for serve in serveList:
        _serve = {}
        _serve['serveId'] = serve.id
        _serve['serveName'] = serve.name
        _serve['serveTelephone'] = serve.telephone
        _serve['everAttachCategory'] = '1' if serve.category != None else '0'
        _serveList.append(_serve)
    response['code'] = 0
    response['data'] = _serveList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def getFreeServeList(request):
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
    serveQuery = Serve.objects.filter(shopId = str(_shopId)).filter(category = None)

    _serveList = []
    for serve in serveQuery:
        _serve = {}
        _serve['serveId'] = serve.id
        _serve['serveName'] = serve.name
        _serve['serveTelephone'] = serve.telephone
        _serve['everAttachCategory'] = '1' if serve.category != None else '0'
        _serveList.append(_serve)
    response['code'] = 0
    response['data'] = _serveList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

