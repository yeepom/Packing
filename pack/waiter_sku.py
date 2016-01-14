#encoding:utf-8
from django.http import HttpResponse
import sys,json
from pack.models import Sku,Category,Waiter
from django.views.decorators.csrf import csrf_exempt
import logging
from django.core.exceptions import ObjectDoesNotExist

reload(sys)
sys.setdefaultencoding('utf8')


@csrf_exempt
def waiterGetShopSkus(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _waiterId = request.session.get('waiterId')
    if not _waiterId:
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
        waiter = Waiter.objects.select_related().get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != waiter.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    shop = waiter.shop
    if  shop == None:
        response['code'] = 2
        response['errorMsg'] = '请先关联账户'
        return HttpResponse(json.dumps(response),content_type="application/json")

    categoryQuery = Category.objects.select_related().filter(shop = shop)
    response_categories = []
    for category in categoryQuery:
        response_category = {}
        response_category['categoryId'] = category.id
        response_category['categoryName'] = category.categoryName
        response_category['categoryType'] = category.categoryType
        skus = category.sku_set.filter(isValid=True).order_by('id')
        response_category_skus = []
        for sku in skus:
            response_category_sku = {}
            response_category_sku['skuId'] = sku.id
            response_category_sku['skuName'] = sku.name.encode('utf-8')
            response_category_sku['skuDesc'] = sku.desc.encode('utf-8')
            _img = sku.img.split(',')

            response_category_sku['skuImg'] = _img[0]
            response_data_sku_size_list = []
            flag = 0
            _priceList = sku.price.split(',')
            _sizeList = sku.size.split(',')
            for _price in _priceList:
                response_category_sku_size = {}
                response_category_sku_size['skuSizeName'] = _sizeList[flag].encode('utf-8')
                response_category_sku_size['skuSizePrice'] = str(_price)
                if flag == 0:
                    response_category_sku['skuPriceDesc'] = str(_price)
                    response_category_sku['skuSizeDesc'] = _sizeList[flag]
                    flag = 1
                response_data_sku_size_list.append(response_category_sku_size)
                response_category_sku['skuSizeList'] = response_data_sku_size_list
            _skuSizeListCount = len(_priceList)
            print _skuSizeListCount
            response_category_sku['skuSizesCount'] = _skuSizeListCount
            if _skuSizeListCount > 1:
                response_category_sku['skuPriceDesc'] = str(_skuSizeListCount)+'种规格'.encode('utf-8')
                response_category_sku['skuSizeDesc'] = str(_skuSizeListCount)+'种规格'.encode('utf-8')
            response_category_skus.append(response_category_sku)
        response_category['skuList'] = response_category_skus
        response_categories.append(response_category)
    response['code'] = 0
    response['data'] = response_categories
    return HttpResponse(json.dumps(response),content_type="application/json")


# @csrf_exempt
# def waiterGetCategories(request):
#     response = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     _waiterId = request.session.get('waiterId')
#     if not _waiterId:
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
#         waiter = Waiter.objects.get(id = _waiterId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != waiter.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _shopId = request.REQUEST.get('shopId')
#     if _shopId == None or _shopId == '':
#         response['code'] = -1
#         response['errorMsg'] = '获取商家信息失败'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     _shopId = str(_shopId)
#     if _shopId != str(waiter.shop.id):
#         response['code'] = -1
#         response['errorMsg'] = '账户不对应'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#
#     categories = Category.objects.filter(shop__id = _shopId).order_by('-id')
#     response_categories = []
#     for category in categories:
#         response_category={}
#         response_category['categoryName'] = category.categoryName
#         response_category['categoryId'] = category.id
#         response_categories.append(response_category)
#     response['code'] = 0
#     response['data'] = response_categories
#     return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#
# @csrf_exempt
# def waiterGetSkusWithCategory(request):
#     response = {}
#     response_data = {}
#     response['data'] = {}
#     response['errorMsg'] = ""
#     _waiterId = request.session.get('waiterId')
#     if not _waiterId:
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
#         waiter = Waiter.objects.get(id = _waiterId)
#     except ObjectDoesNotExist:
#         response['code'] = 1
#         response['errorMsg'] = '请先登录'
#         return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
#     if _lastLoginTime != waiter.lastLoginTime:
#         response['code'] = 1
#         response['errorMsg'] = '上次登录失效，请重新登录'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     ####################END#################
#
#     _categoryId =request.REQUEST.get('categoryId')
#     if _categoryId == None or _categoryId == '':
#         response['code'] = -1
#         response['errorMsg'] = '获取品类id失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#     _categoryId = str(_categoryId)
#     try:
#         category = Category.objects.get(id = _categoryId)
#     except ObjectDoesNotExist:
#         response['code'] = -1
#         response['errorMsg'] = '查找category失败'
#         return HttpResponse(json.dumps(response),content_type="application/json")
#
#     skus = category.sku_set.filter(isValid=True).order_by('-id')
#     response_data_skus = []
#     for sku in skus:
#         response_data_sku = {}
#         response_data_sku['skuId'] = sku.id
#         response_data_sku['skuName'] = sku.name.encode('utf-8')
#         response_data_sku['skuDesc'] = sku.desc.encode('utf-8')
#         _img = sku.img.split(',')
#         response_data_sku['skuImg'] = _img[0]
#         _skuSizeList = sku.skusize_set.all()
#         response_data_sku_size_list = []
#         for skuSize in _skuSizeList:
#             response_data_sku_size = {}
#             response_data_sku_size['skuSizeId'] = skuSize.id
#             response_data_sku_size['skuSizeName'] = skuSize.name.encode('utf-8')
#             response_data_sku_size['skuPrice'] = str(skuSize.price)
#             response_data_sku_size_list.append(response_data_sku_size)
#         response_data_sku['skuSizeList'] = response_data_sku_size_list
#         response_data_skus.append(response_data_sku)
#     response_data['skus'] = response_data_skus
#     response['code'] = 0
#     response['data'] = response_data_skus
#     return HttpResponse(json.dumps(response),content_type="application/json")
