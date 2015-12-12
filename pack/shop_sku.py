#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Sku,Category,Cook
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')


@csrf_exempt
def getCategories(request):
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

    categories = Category.objects.filter(shop = shop).order_by('-id')
    response_categories = []
    for category in categories:
        response_category={}
        response_category['categoryName'] = category.categoryName
        response_category['categoryId'] = category.id
        response_category['cookDispatchUnit'] = category.dispatchUnit
        response_category['cookListCount'] = category.cook_set.count()
        response_categories.append(response_category)
    response['code'] = 0
    response['data'] = response_categories
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def addCategory(request):
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

    _categoryName = request.REQUEST.get('categoryName')
    _dispatchUnit = request.REQUEST.get('cookDispatchUnit')
    _cookList = request.REQUEST.getlist('cookList[]')
    logger.info(_cookList)
    logger.info(type(_cookList))
    if _categoryName == None or _categoryName == '':
        response['code'] = -1
        response['errorMsg'] = '请输入名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _dispatchUnit == None or _dispatchUnit == '':
        response['code'] = -1
        response['errorMsg'] = '请输入平均分配个数'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _dispatchUnit.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '分配个数应该为整数'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _cookList == None or _cookList == '':
        response['code'] = -1
        response['errorMsg'] = '获取skuList失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _categoryName = str(_categoryName)
    _dispatchUnit = int(_dispatchUnit)
    # _cookList = json.loads(_cookList)

    category = Category(categoryName = _categoryName,shop = shop,dispatchUnit = _dispatchUnit)
    try:
        category.save()
    except Exception,e:
        print('e')
        response['code'] = -1
        response['errorMsg'] = '保存类别失败'
        return HttpResponse(json.dumps(response),content_type="application/json")
    for _cookId in _cookList:
        # _cookId = _cook['cookId']
        _cookId = str(_cookId)
        try:
            cook = Cook.objects.get(id = _cookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取serve失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        cook.category = category
        cook.save()
    response['code'] = 0
    response_category = {}
    response_category['categoryName'] = category.categoryName
    response_category['categoryId'] = category.id
    response_category['cookDispatchUnit'] = category.dispatchUnit
    response_category['cookListCount'] = category.cook_set.count()
    response['data'] = response_category
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def alterCategory(request):
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
    if _method == '0':
        _categoryId = request.REQUEST.get('categoryId')
        _categoryName = request.REQUEST.get('categoryName')
        if _categoryName == None or _categoryName == '':
            response['code'] = -1
            response['errorMsg'] = '请输入名字'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _categoryId == None or _categoryId == '':
            response['code'] = -1
            response['errorMsg'] = '请输入类别id'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        _categoryId = str(_categoryId)
        _categoryName = str(_categoryName)
        try:
            category = Category.objects.get(id = _categoryId)
        except ObjectDoesNotExist:
            response['code'] = 1
            response['errorMsg'] = '获取类别失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        category.categoryName = _categoryName
        category.save()
        try:
            category.save()
        except Exception,e:
            print('e')
            response['code'] = -1
            response['errorMsg'] = '保存类别失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        response['code'] = 0
        response_category = {}
        response_category['categoryName'] = category.categoryName
        response_category['categoryId'] = category.id
        response_category['cookDispatchUnit'] = category.dispatchUnit
        response_category['cookListCount'] = category.cook_set.count()
        response['data'] = response_category
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _method == '1':
        _categoryId = request.REQUEST.get('categoryId')
        _dispatchUnit = request.REQUEST.get('cookDispatchUnit')
        if _categoryId == None or _categoryId == '':
            response['code'] = -1
            response['errorMsg'] = '请输入类别id'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _dispatchUnit == None or _dispatchUnit == '':
            response['code'] = -1
            response['errorMsg'] = '请输入平均分配个数'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _dispatchUnit.isdigit() == False:
            response['code'] = -1
            response['errorMsg'] = '分配个数应该为整数'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        _categoryId = str(_categoryId)
        _dispatchUnit = int(_dispatchUnit)
        try:
            category = Category.objects.get(id = _categoryId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取类别失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        category.dispatchUnit = _dispatchUnit
        category.save()
        try:
            category.save()
        except Exception,e:
            print('e')
            response['code'] = -1
            response['errorMsg'] = '保存类别失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        response['code'] = 0
        response_category = {}
        response_category['categoryName'] = category.categoryName
        response_category['categoryId'] = category.id
        response_category['cookDispatchUnit'] = category.dispatchUnit
        response_category['cookListCount'] = category.cook_set.count()
        response['data'] = response_category
        return HttpResponse(json.dumps(response),content_type="application/json")

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
    response_cookList = []
    for _cookId in _cookList:
        _cookId = str(_cookId)
        try:
            cook = Cook.objects.get(id = _cookId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取serve失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        cook.category = category
        cook.save()
        _cook = {}
        _cook['cookId'] = cook.id
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
        response_cookList.append(_cook)
    response['code'] = 0
    response['data'] = response_cookList
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
        response['errorMsg'] = '获取serveId失败'
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
    if cookCount == 1:
        response['code'] = -1
        response['errorMsg'] = '至少有一个厨师'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

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
def getSkusWithCategory(request):
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

    _categoryId =request.REQUEST.get('categoryId')
    if _categoryId == None or _categoryId == '':
        response['code'] = -1
        response['errorMsg'] = '获取品类id失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    try:
        category = Category.objects.get(id = str(_categoryId))
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '查找category失败'
        return HttpResponse(json.dumps(response),content_type="application/json")

    skus = category.sku_set.filter(isValid=True).order_by('-id')
    response_data_skus = []
    for sku in skus:
        response_data_sku = {}
        response_data_sku['skuId'] = sku.id
        response_data_sku['skuName'] = sku.name.encode('utf-8')
        response_data_sku['skuDesc'] = sku.desc.encode('utf-8')
        _img = sku.img.split(',')
        response_data_sku['skuImg'] = _img[0]
        response_data_sku_size_list = []
        flag = 0
        _priceList = sku.price.split(',')
        _sizeList = sku.size.split(',')
        for _price in _priceList:
            response_data_sku_size = {}
            response_data_sku_size['skuSizeName'] = _sizeList[flag].encode('utf-8')
            response_data_sku_size['skuSizePrice'] = str(_price)
            if flag == 0:
                response_data_sku['skuPriceDesc'] = str(_price)
                response_data_sku['skuSizeDesc'] = _sizeList[flag].encode('utf-8')
            response_data_sku_size_list.append(response_data_sku_size)
            response_data_sku['skuSizeList'] = response_data_sku_size_list
            flag = flag+1
        _skuSizeListCount = len(_priceList)
        response_data_sku['skuSizesCount'] = _skuSizeListCount
        if _skuSizeListCount > 1:
            response_data_sku['skuPriceDesc'] = str(_skuSizeListCount)+'种规格'.encode('utf-8')
            response_data_sku['skuSizeDesc'] = str(_skuSizeListCount)+'种规格'.encode('utf-8')

        response_data_skus.append(response_data_sku)

    # response_data['skusList'] = response_data_skus
    response['code'] = 0
    response['data'] = response_data_skus
    return HttpResponse(json.dumps(response),content_type="application/json")



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

@csrf_exempt
def skuInfo(request):
    logger = logging.getLogger('Pack.app')
    logger.info(request)
    response = {}
    response_data = {}
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

    #if method = 0 , add;method=1, update ; method = 3, delete
    if _method == '0':
        _name = request.REQUEST.get('skuName')
        _desc = request.REQUEST.get('skuDesc')
        _categoryId = request.REQUEST.get('categoryId')
        _img = request.REQUEST.get('skuImg')
        _skuSizeNameList = request.REQUEST.getlist('skuSizeNameList[]')
        _skuSizePriceList = request.REQUEST.getlist('skuSizePriceList[]')
        
        if _name == None or _name == '':
            response['code'] = -1
            response['errorMsg'] = '请输入名字'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if _desc == None:
            _desc = ''
        if _categoryId == None or _categoryId == '':
            response['code'] = -1
            response['errorMsg'] = '请选择品类'
            return HttpResponse(json.dumps(response),content_type="application/json")
        _skuSizeNameListCount = len(_skuSizeNameList)
        _skuSizePriceListCount = len(_skuSizePriceList)
        logger.info(_skuSizeNameList)
        logger.info(_skuSizePriceList)
        logger.info(type(_skuSizeNameList))
        logger.info(type(_skuSizePriceList))
        if  _skuSizeNameListCount != _skuSizePriceListCount:
            response['code'] = -1
            response['errorMsg'] = 'sizename与sizeprice不对应'
            return HttpResponse(json.dumps(response),content_type="application/json")

        try:
            category = Category.objects.get(id = str(_categoryId))
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取品类失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        if category.shop.id != _shopId:
            response['code'] = -1
            response['errorMsg'] = '获取品类失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        _price = ''
        _size = ''
        response_data_skuSize_list = []
        for index in range(_skuSizeNameListCount):
            if index == 0:
                _price = str(_skuSizePriceList[index])
                _size = str(_skuSizeNameList[index])
            else:
                _price = _price+','+str(_skuSizePriceList[index])
                _size = _size+','+str(_skuSizeNameList[index])
            response_data_skuSize = {}
            response_data_skuSize['skuSizeName'] = _skuSizeNameList[index]
            response_data_skuSize['skuSizePrice'] = _skuSizePriceList[index]
            response_data_skuSize_list.append(response_data_skuSize)
        # flag = 0
        # for _skuSize in _skuSizeNameList:
        #     if flag == 0:
        #         _price = _skuSize['skuPrice']
        #         _size = _skuSize['skuSizeName']
        #         response_data['skuPriceDesc'] = _price
        #         response_data['skuSizeDesc'] = _size
        #     else:
        #         _price = _price+','+ _skuSize['skuPrice']
        #         _size = _size+','+_skuSize['skuSizeName']
        #     flag = flag+1
        sku = Sku(name = _name, desc = _desc, img = _img,price = _price,size = _size,category = category)
        sku.save()
        response_data['skuId'] = sku.id
        response_data['skuName'] = sku.name.encode('utf-8')
        response_data['skuDesc'] = sku.desc.encode('utf-8')
        response_data['skuImg'] = sku.img
        # if flag > 1:
        #     response_data['skuPriceDesc'] = str(flag)+'种规格'.encode('utf-8')
        #     response_data['skuSizeDesc'] = str(flag)+'种规格'.encode('utf-8')
        response_data['skuSizesCount'] = _skuSizeNameListCount
        response_data['skuSizeList'] = response_data_skuSize_list
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _method == '1':
        _skuId = request.REQUEST.get('skuId')
        _name = request.REQUEST.get('skuName')
        _desc = request.REQUEST.get('skuDesc')
        _img = request.REQUEST.get('skuImg')

        _skuSizeNameList = request.REQUEST.getlist('skuSizeNameList[]')
        _skuSizePriceList = request.REQUEST.getlist('skuSizePriceList[]')
        # __skuSizeList = json.loads(_skuSizeList)

        if _skuId == None or _skuId == '':
            response['code'] = -1
            response['errorMsg'] = '请输入skuId'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if _name == None or _name == '':
            response['code'] = -1
            response['errorMsg'] = '请输入名字'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if _desc == None:
            _desc = ''
        _skuSizeNameListCount = len(_skuSizeNameList)
        _skuSizePriceListCount = len(_skuSizePriceList)
        logger.info(_skuSizeNameList)
        logger.info(_skuSizePriceList)
        logger.info(type(_skuSizeNameList))
        logger.info(type(_skuSizePriceList))
        if  _skuSizeNameListCount != _skuSizePriceListCount:
            response['code'] = -1
            response['errorMsg'] = 'sizename与sizeprice不对应'
            return HttpResponse(json.dumps(response),content_type="application/json")

        _skuId = str(_skuId)
        try:
            sku = Sku.objects.get(id = _skuId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '获取sku失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        _price = ''
        _size = ''
        response_data_skuSize_list = []
        for index in range(_skuSizeNameListCount):
            if index == 0:
                _price = str(_skuSizePriceList[index])
                _size = str(_skuSizeNameList[index])
            else:
                _price = _price+','+str(_skuSizePriceList[index])
                _size = _size+','+str(_skuSizeNameList[index])
            response_data_skuSize = {}
            response_data_skuSize['skuSizeName'] = _skuSizeNameList[index]
            response_data_skuSize['skuSizePrice'] = _skuSizePriceList[index]
            response_data_skuSize_list.append(response_data_skuSize)
        sku.name = _name
        sku.desc = _desc
        sku.img = _img
        sku.price = _price
        sku.size = _size
        sku.save()
        response_data = {}
        response_data['skuId'] = sku.id
        response_data['skuName'] = sku.name.encode('utf-8')
        response_data['skuDesc'] = sku.desc.encode('utf-8')
        response_data['skuImg'] = sku.img
        # if flag > 1:
        #     response_data['skuPriceDesc'] = str(flag)+'种规格'.encode('utf-8')
        #     response_data['skuSizeDesc'] = str(flag)+'种规格'.encode('utf-8')
        response_data['skuSizesCount'] = _skuSizeNameListCount
        response_data['skuSizeList'] = response_data_skuSize_list
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '3':
        _skuId = request.REQUEST.get('skuId')
        if _skuId == None or _skuId == '':
            response['code'] = -1
            response['errorMsg'] = '商品id为空'
            return HttpResponse(json.dumps(response),content_type="application/json")

        try:
            sku = Sku.objects.get(id = _skuId)
        except ObjectDoesNotExist:
            response['code'] = -1
            response['errorMsg'] = '商品查询失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        sku.isValid = False
        sku.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
#
# @csrf_exempt
# def alterSkuName(request):
#     logger = logging.getLogger('Pack.app')
#     logger.info(request.REQUEST)
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     response_data = {}
#     _shopId = request.session.get('shopId')
#     _shopId = str(_shopId)
#     if not _shopId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         shop = Shop.objects.get(id = _shopId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != shop.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _skuId = request.REQUEST.get('skuId')
#     _skuName = request.REQUEST.get('skuName')
#
#     if _skuId == None or _skuId == '':
#         response['code'] = -1
#         response['errorMsg'] = '商品id为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuName == None or _skuName == '':
#         response['code'] = -1
#         response['errorMsg'] = '请输入名字'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _skuId = str(_skuId)
#     _skuName = str(_skuName)
#
#     try:
#         sku = Sku.objects.get(id = _skuId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '商品查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     sku.name = _skuName
#     sku.save()
#     response['code'] = 0
#     response['data'] = sku.name.encode('utf-8')
#     return HttpResponse(json.dumps(response),content_type="application/json")
#
#
# @csrf_exempt
# def alterSkuImg(request):
#     logger = logging.getLogger('Pack.app')
#     logger.info(request.REQUEST)
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     response_data = {}
#     _shopId = request.session.get('shopId')
#     _shopId = str(_shopId)
#     if not _shopId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         shop = Shop.objects.get(id = _shopId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != shop.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _skuId = request.REQUEST.get('skuId')
#     _skuImg = request.REQUEST.get('skuImg')
#
#     if _skuId == None or _skuId == '':
#         response['code'] = -1
#         response['errorMsg'] = '商品id为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuImg == None or _skuImg == '':
#         response['code'] = -1
#         response['errorMsg'] = '图片url为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _skuId = str(_skuId)
#     _skuImg = str(_skuImg)
#
#     try:
#         sku = Sku.objects.get(id = _skuId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '商品查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     sku.img = _skuImg
#     sku.save()
#     response['code'] = 0
#     response['data'] = sku.img
#     return HttpResponse(json.dumps(response),content_type="application/json")
#
# @csrf_exempt
# def addSkuSize(request):
#     logger = logging.getLogger('Pack.app')
#     logger.info(request.REQUEST)
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     response_data = {}
#     _shopId = request.session.get('shopId')
#     _shopId = str(_shopId)
#     if not _shopId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         shop = Shop.objects.get(id = _shopId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != shop.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _skuId = request.REQUEST.get('skuId')
#     _skuSizeName = request.REQUEST.get('skuSizeName')
#     _skuSizePrice = request.REQUEST.get('skuSizePrice')
#
#     if _skuId == None or _skuId == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuSizeName == None or _skuSizeName == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuSizePrice == None or _skuSizePrice == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _skuId = str(_skuId)
#     _skuSizeName = str(_skuSizeName)
#     _skuSizePrice = str(_skuSizePrice)
#
#     try:
#         sku = Sku.objects.get(id = _skuId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '商品查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     skuSize = SkuSize(name = _skuSizeName, price = _skuSizePrice, sku = sku)
#     skuSize.save()
#     response['code'] = 0
#     response_data['skuSizeId'] = skuSize.id
#     response_data['skuSizeName'] = skuSize.name.encode('utf-8')
#     response_data['skuSizePrice'] = str(skuSize.price)
#     response['data'] = response_data
#     return HttpResponse(json.dumps(response),content_type="application/json")
#
#
# @csrf_exempt
# def alterSkuSize(request):
#     logger = logging.getLogger('Pack.app')
#     logger.info(request.REQUEST)
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     response_data = {}
#     _shopId = request.session.get('shopId')
#     _shopId = str(_shopId)
#     if not _shopId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         shop = Shop.objects.get(id = _shopId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != shop.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _skuSizeId = request.REQUEST.get('skuSizeId')
#     _skuSizeName = request.REQUEST.get('skuSizeName')
#     _skuSizePrice = request.REQUEST.get('skuSizePrice')
#
#     if _skuSizeId == None or _skuSizeId == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuSizeName == None or _skuSizeName == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if _skuSizePrice == None or _skuSizePrice == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _skuSizeId = str(_skuSizeId)
#     _skuSizeName = str(_skuSizeName)
#     _skuSizePrice = str(_skuSizePrice)
#
#     try:
#         skuSize = SkuSize.objects.get(id = _skuSizeId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '类型查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     skuSize.name = _skuSizeName
#     skuSize.price = _skuSizePrice
#     skuSize.save()
#     response['code'] = 0
#     response_data['skuSizeId'] = skuSize.id
#     response_data['skuSizeName'] = skuSize.name.encode('utf-8')
#     response_data['skuSizePrice'] = str(skuSize.price)
#     response['data'] = response_data
#     return HttpResponse(json.dumps(response),content_type="application/json")
#
#
# @csrf_exempt
# def delSkuSize(request):
#     logger = logging.getLogger('Pack.app')
#     logger.info(request.REQUEST)
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     _shopId = request.session.get('shopId')
#     _shopId = str(_shopId)
#     if not _shopId:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ##################JUDGE############
#     _lastLoginTime = request.session.get('lastLoginTime')
#     if not _lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         shop = Shop.objects.get(id = _shopId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != shop.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _skuId = request.REQUEST.get('skuId')
#     _skuSizeId = request.REQUEST.get('skuSizeId')
#
#     if _skuId == None or _skuId == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     if _skuSizeId == None or _skuSizeId == '':
#         response['code'] = -1
#         response['errorMsg'] = 'skuSizeId为空'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _skuId = str(_skuId)
#     _skuSizeId = str(_skuSizeId)
#     try:
#         sku = Sku.objects.get(id = _skuId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '商品查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     skuSizeCount = sku.skusize_set.count()
#     if skuSizeCount == 1:
#         response['code'] = -1
#         response['errorMsg'] = '至少有一个商品类型'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     try:
#         skuSize = SkuSize.objects.get(id = _skuSizeId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = 'skuSize查询失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     if skuSize.sku == sku:
#         skuSize.delete()
#         response['code'] = 0
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     else:
#         response['code'] = -1
#         response['errorMsg'] = 'sku与skuSize不对应'
#         return HttpResponse(json.dumps(response),content_type="application/json")


