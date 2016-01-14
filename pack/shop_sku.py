#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Shop,Sku,Category,Cook,OrderSeparate,BeforeCook,AfterCook
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
        response_category['categoryId'] = str(str(category.id))
        response_category['categoryType'] = category.categoryType
        response_category['orderSeparateListCount'] = category.orderseparate_set.count()
        response_category['beforeCookListCount'] = category.beforecook_set.count()
        response_category['afterCookListCount'] = category.aftercook_set.count()
        response_categories.append(response_category)
    response['code'] = 0
    response['data'] = response_categories
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def addCategory(request):
    logger = logging.getLogger('Pack.app')
    # logger.info(request)
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
    _categoryType = request.REQUEST.get('categoryType')

    if _categoryName == None or _categoryName == '':
        response['code'] = -1
        response['errorMsg'] = '请输入名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _categoryType == None or _categoryType == '':
        response['code'] = -1
        response['errorMsg'] = '请输入类型'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    ##类别0：配单+前打荷+后打荷+上菜员
    if _categoryType == '0':
        _orderSeparateList = request.REQUEST.getlist('orderSeparateList[]')
        _beforeCookList = request.REQUEST.getlist('beforeCookList[]')
        _afterCookList = request.REQUEST.getlist('afterCookList[]')
        if _orderSeparateList == []:
            response['code'] = -1
            response['errorMsg'] = '获取配菜员列表失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _beforeCookList == []:
            response['code'] = -1
            response['errorMsg'] = '获取前打荷列表失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _afterCookList == []:
            response['code'] = -1
            response['errorMsg'] = '获取后打荷列表失败'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        category = Category(categoryName = _categoryName,shop = shop,categoryType = _categoryType)
        try:
            category.save()
        except Exception,e:
            print('e')
            response['code'] = -1
            response['errorMsg'] = '保存类别失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        for _orderSeparateId in _orderSeparateList:
            _orderSeparateId = str(_orderSeparateId)
            try:
                orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取配菜员失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if orderSeparate.category != None:
                response['code'] = -1
                response['errorMsg'] = '有配菜员已经关联其他类别'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

            orderSeparate.category = category
            orderSeparate.save()
        for _beforeCookId in _beforeCookList:
            _beforeCookId = str(_beforeCookId)
            try:
                beforeCook = BeforeCook.objects.get(id = _beforeCookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取前打荷失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if beforeCook.category != None:
                response['code'] = -1
                response['errorMsg'] = '有前打荷已经关联其他类别'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            beforeCook.category = category
            beforeCook.save()
        for _afterCookId in _afterCookList:
            _afterCookId = str(_afterCookId)
            try:
                afterCook = AfterCook.objects.get(id = _afterCookId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取后打荷失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if afterCook.category != None:
                response['code'] = -1
                response['errorMsg'] = '有后打荷已经关联其他类别'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            afterCook.category = category
            afterCook.save()

        response['code'] = 0
        response_category = {}
        response_category['categoryName'] = category.categoryName
        response_category['categoryId'] = str(category.id)
        response_category['categoryType'] = category.categoryType
        response_category['orderSeparateListCount'] = category.orderseparate_set.count()
        response_category['beforeCookListCount'] = category.beforecook_set.count()
        response_category['afterCookListCount'] = category.aftercook_set.count()
        response['data'] = response_category
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _categoryType == '1':
            ##类别1：配单+上菜员
        _orderSeparateList = request.REQUEST.getlist('orderSeparateList[]')
        if _orderSeparateList == []:
            response['code'] = -1
            response['errorMsg'] = '请添加配菜员'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        category = Category(categoryName = _categoryName,shop = shop,categoryType = _categoryType)
        try:
            category.save()
        except Exception,e:
            print('e')
            response['code'] = -1
            response['errorMsg'] = '保存类别失败'
            return HttpResponse(json.dumps(response),content_type="application/json")
        for _orderSeparateId in _orderSeparateList:
            _orderSeparateId = str(_orderSeparateId)
            try:
                orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
            except ObjectDoesNotExist:
                response['code'] = -1
                response['errorMsg'] = '获取配菜员失败'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            if orderSeparate.category != None:
                response['code'] = -1
                response['errorMsg'] = '有配菜员已经关联其他类别'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

            orderSeparate.category = category
            orderSeparate.save()

        response['code'] = 0
        response_category = {}
        response_category['categoryName'] = category.categoryName
        response_category['categoryId'] = str(category.id)
        response_category['categoryType'] = category.categoryType
        response_category['orderSeparateListCount'] = category.orderseparate_set.count()
        response['data'] = response_category
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _categoryType == '2':
        ##类别2：上菜员
        category = Category(categoryName = _categoryName,shop = shop,categoryType = _categoryType)
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
        response_category['categoryId'] = str(category.id)
        response_category['categoryType'] = category.categoryType
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
        response_category['categoryId'] = str(category.id)
        response_category['categoryType'] = category.categoryType
        response_category['orderSeparateListCount'] = category.orderseparate_set.count()
        response_category['beforeCookListCount'] = category.beforecook_set.count()
        response_category['afterCookListCount'] = category.aftercook_set.count()
        response['data'] = response_category
        return HttpResponse(json.dumps(response),content_type="application/json")


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
        response_data_sku['skuId'] = str(sku.id)
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
        if _skuSizeNameList == []:
            response['code'] = -1
            response['errorMsg'] = '请添加规格'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if _skuSizePriceList == []:
            response['code'] = -1
            response['errorMsg'] = '请添加价格'
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

        sku = Sku(name = _name, desc = _desc, img = _img,price = _price,size = _size,category = category)
        sku.save()
        response_data['skuId'] = str(sku.id)
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
        if _skuSizeNameList == []:
            response['code'] = -1
            response['errorMsg'] = '请添加规格'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if _skuSizePriceList == []:
            response['code'] = -1
            response['errorMsg'] = '请添加价格'
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
        response_data['skuId'] = str(sku.id)
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
