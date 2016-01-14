#encoding:utf-8
from django.http import HttpResponse
from pack.models import Shop,Waiter,Cook,Serve,Order,OrderSku,OrderSeparate,BeforeCook,AfterCook
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
import sys,re,json

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def getMemberList(request):
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

    waiterList = shop.waiter_set.all().order_by('-id')
    _waiterList = []
    for waiter in waiterList:
        _waiter = {}
        _waiter['waiterId'] = str(waiter.id)
        _waiter['waiterName'] = waiter.name
        _waiter['waiterTelephone'] = waiter.telephone
        _waiterList.append(_waiter)
    response_data['waiterList'] = _waiterList

    orderSeparateQuery = OrderSeparate.objects.filter(shopId = str(_shopId)).order_by('-id')
    _orderSeparateList = []
    for orderSeparate in orderSeparateQuery:
        _orderSeparate = {}
        _orderSeparate['orderSeparateId'] = str(orderSeparate.id)
        _orderSeparate['orderSeparateName'] = orderSeparate.name
        _orderSeparate['orderSeparateTelephone'] = orderSeparate.telephone
        _orderSeparate['everAttachCategory'] = '1' if orderSeparate.category != None else '0'
        _orderSeparateList.append(_orderSeparate)
    response_data['orderSeparateList'] = _orderSeparateList

    beforeCookQuery = BeforeCook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _beforeCookList = []
    for beforeCook in beforeCookQuery:
        _beforeCook = {}
        _beforeCook['beforeCookId'] = str(beforeCook.id)
        _beforeCook['beforeCookName'] = beforeCook.name
        _beforeCook['beforeCookTelephone'] = beforeCook.telephone
        _beforeCook['everAttachCategory'] = '1' if beforeCook.category != None else '0'
        _beforeCookList.append(_beforeCook)
    response_data['beforeCookList'] = _beforeCookList

    afterCookQuery = AfterCook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _afterCookList = []
    for afterCook in afterCookQuery:
        _afterCook = {}
        _afterCook['afterCookId'] = str(afterCook.id)
        _afterCook['afterCookName'] = afterCook.name
        _afterCook['afterCookTelephone'] = afterCook.telephone
        _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
        _afterCookList.append(_afterCook)
    response_data['afterCookList'] = _afterCookList

    serveList = shop.serve_set.all().order_by('-id')
    _serveList = []
    for serve in serveList:
        _serve = {}
        _serve['serveId'] = str(serve.id)
        _serve['serveName'] = serve.name
        _serve['serveTelephone'] = serve.telephone
        _serveList.append(_serve)
    response_data['serveList'] = _serveList

    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def getWaiterList(request):
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

    waiterList = shop.waiter_set.all().order_by('-id')
    _waiterList = []
    for waiter in waiterList:
        _waiter = {}
        _waiter['waiterId'] = str(waiter.id)
        _waiter['waiterName'] = waiter.name
        _waiter['waiterTelephone'] = waiter.telephone
        _waiterList.append(_waiter)
    response['code'] = 0
    response['data'] = _waiterList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def getOrderSeparateList(request):
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

    orderSeparateQuery = OrderSeparate.objects.filter(shopId = str(_shopId)).order_by('-id')
    _orderSeparateList = []
    for orderSeparate in orderSeparateQuery:
        _orderSeparate = {}
        _orderSeparate['orderSeparateId'] = str(orderSeparate.id)
        _orderSeparate['orderSeparateName'] = orderSeparate.name
        _orderSeparate['orderSeparateTelephone'] = orderSeparate.telephone
        _orderSeparate['everAttachCategory'] = '1' if orderSeparate.category != None else '0'
        _orderSeparateList.append(_orderSeparate)

    response['code'] = 0
    response['data'] = _orderSeparateList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def getBeforeCookList(request):
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

    beforeCookQuery = BeforeCook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _beforeCookList = []
    for beforeCook in beforeCookQuery:
        _beforeCook = {}
        _beforeCook['beforeCookId'] = str(beforeCook.id)
        _beforeCook['beforeCookName'] = beforeCook.name
        _beforeCook['beforeCookTelephone'] = beforeCook.telephone
        _beforeCook['everAttachCategory'] = '1' if beforeCook.category != None else '0'
        _beforeCookList.append(_beforeCook)
    response['code'] = 0
    response['data'] = _beforeCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def getAfterCookList(request):
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

    afterCookQuery = AfterCook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _afterCookList = []
    for afterCook in afterCookQuery:
        _afterCook = {}
        _afterCook['afterCookId'] = str(afterCook.id)
        _afterCook['afterCookName'] = afterCook.name
        _afterCook['afterCookTelephone'] = afterCook.telephone
        _afterCook['everAttachCategory'] = '1' if afterCook.category != None else '0'
        _afterCookList.append(_afterCook)
    response['code'] = 0
    response['data'] = _afterCookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def getCookList(request):
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

    cookQuery = Cook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _cookList = []
    for cook in cookQuery:
        _cook = {}
        _cook['cookId'] = str(cook.id)
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
        _cook['everAttachCategory'] = '1' if cook.category != None else '0'
        _cookList.append(_cook)
    response['code'] = 0
    response['data'] = _cookList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def getServeList(request):
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
    serveQuery = Serve.objects.filter(shopId = str(_shopId)).order_by('-id')

    _serveList = []
    for serve in serveQuery:
        _serve = {}
        _serve['serveId'] = str(serve.id)
        _serve['serveName'] = serve.name
        _serve['serveTelephone'] = serve.telephone
        _serveList.append(_serve)
    response['code'] = 0
    response['data'] = _serveList
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def verifyWaiter(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_wait_order = Waiter.objects.filter(telephone = _telephone)
    if not query_wait_order.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        waiter = Waiter(telephone = _telephone, name = _name, headImage = _headImage,shop = shop)
        waiter.save()
        response['code'] = 0
        response_data = {}
        response_data['waiterId'] = str(waiter.id)
        response_data['waiterName'] = waiter.name
        response_data['waiterTelephone'] = waiter.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    waiter = query_wait_order[0]
    if waiter.shop == None:
        waiter.shop = shop
        waiter.save()
        response['code'] = 0
        response_data = {}
        response_data['waiterId'] = str(waiter.id)
        response_data['waiterName'] = waiter.name
        response_data['waiterTelephone'] = waiter.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    elif waiter.shop == shop:
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")



@csrf_exempt
def removeWaiter(request):
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

    _waiterId = request.REQUEST.get('waiterId')
    if _waiterId == None or _waiterId == '':
        response['code'] = -1
        response['errorMsg'] = '获取waiterOrerId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _waiterId = str(_waiterId)
    try:
        waiter = Waiter.objects.get(id = _waiterId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取waiterOrer失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if waiter.shop == shop:
        orderQuery = Order.objects.filter(waiterId = str(str(waiter.id))).filter(status = '0')
        if orderQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该服务员有未完成订单'
            return HttpResponse(json.dumps(response),content_type="application/json")
        waiter.shop = None
        waiter.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def verifyOrderSeparate(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_orderSepa_order = OrderSeparate.objects.filter(telephone = _telephone)
    if not query_orderSepa_order.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        orderSeparate = OrderSeparate(telephone = _telephone, name = _name, headImage = _headImage,shopId = str(shop.id))
        orderSeparate.save()
        response['code'] = 0
        response_data = {}
        response_data['orderSeparateId'] = str(orderSeparate.id)
        response_data['orderSeparateName'] = orderSeparate.name
        response_data['orderSeparateTelephone'] = orderSeparate.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    orderSeparate = query_orderSepa_order[0]
    if orderSeparate.shopId == "":
        orderSeparate.shopId = str(shop.id)
        orderSeparate.category = None
        orderSeparate.save()
        response['code'] = 0
        response_data = {}
        response_data['orderSeparateId'] = str(orderSeparate.id)
        response_data['orderSeparateName'] = orderSeparate.name
        response_data['orderSeparateTelephone'] = orderSeparate.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    elif orderSeparate.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeOrderSeparate(request):
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

    _orderSeparateId = request.REQUEST.get('orderSeparateId')
    if _orderSeparateId == None or _orderSeparateId == '':
        response['code'] = -1
        response['errorMsg'] = '获取orderSeparateId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _orderSeparateId = str(_orderSeparateId)
    try:
        orderSeparate = OrderSeparate.objects.get(id = _orderSeparateId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取orderSeparate失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if orderSeparate.shopId == str(shop.id):
        orderSkuQuery = OrderSku.objects.filter(orderSeparateId = str(str(orderSeparate.id))).filter(status = '2')
        if orderSkuQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该配菜员正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if orderSeparate.category == None:
            orderSeparate.shopId = ''
            orderSeparate.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '请在品类中将该配菜员解绑，然后可以删除'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def verifyBeforeCook(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_beforeCook_order = BeforeCook.objects.filter(telephone = _telephone)
    if not query_beforeCook_order.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        beforeCook = BeforeCook(telephone = _telephone, name = _name, headImage = _headImage,shopId = str(shop.id))
        beforeCook.save()
        response['code'] = 0
        response_data = {}
        response_data['beforeCookId'] = str(beforeCook.id)
        response_data['beforeCookName'] = beforeCook.name
        response_data['beforeCookTelephone'] = beforeCook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    beforeCook = query_beforeCook_order[0]
    if beforeCook.shopId == "":
        beforeCook.shopId = str(shop.id)
        beforeCook.category = None
        beforeCook.save()
        response['code'] = 0
        response_data = {}
        response_data['beforeCookId'] = str(beforeCook.id)
        response_data['beforeCookName'] = beforeCook.name
        response_data['beforeCookTelephone'] = beforeCook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    elif beforeCook.shopId ==str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def removeBeforeCook(request):
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

    _beforeCookId = request.REQUEST.get('beforeCookId')
    if _beforeCookId == None or _beforeCookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取beforeCookId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _beforeCookId = str(_beforeCookId)
    try:
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取beforeCook失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if beforeCook.shopId == str(shop.id):
        orderSkuQuery = OrderSku.objects.filter(beforeCookId = str(str(beforeCook.id))).filter(status = '4')
        if orderSkuQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该前打荷正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if beforeCook.category == None:
            beforeCook.shopId = ''
            beforeCook.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '请在品类中将该前打荷解绑，然后可以删除'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def verifyAfterCook(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_afterCook_order = AfterCook.objects.filter(telephone = _telephone)
    if not query_afterCook_order.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        afterCook = AfterCook(telephone = _telephone, name = _name, headImage = _headImage,shopId = str(shop.id))
        afterCook.save()
        response['code'] = 0
        response_data = {}
        response_data['afterCookId'] = str(afterCook.id)
        response_data['afterCookName'] = afterCook.name
        response_data['afterCookTelephone'] = afterCook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    afterCook = query_afterCook_order[0]
    if afterCook.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif afterCook.shopId == "":
        afterCook.shopId = str(shop.id)
        afterCook.save()
        afterCook.category = None
        response['code'] = 0
        response_data = {}
        response_data['afterCookId'] = str(afterCook.id)
        response_data['afterCookName'] = afterCook.name
        response_data['afterCookTelephone'] = afterCook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeAfterCook(request):
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

    _afterCookId = request.REQUEST.get('afterCookId')
    if _afterCookId == None or _afterCookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取后打荷失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _afterCookId = str(_afterCookId)
    try:
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取后打荷失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if afterCook.shopId == str(shop.id):
        orderSkuQuery = OrderSku.objects.filter(afterCookId = str(str(afterCook.id))).filter(status = '6')
        if orderSkuQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该后荷正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if afterCook.category == None:
            afterCook.shopId = ''
            afterCook.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '请在品类中将该后打荷解绑，然后可以删除'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def verifyCook(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_cook = Cook.objects.filter(telephone = _telephone)
    if not query_cook.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        cook = Cook(telephone = _telephone, name = _name, headImage = _headImage,shopId = str(shop.id))
        cook.save()
        response['code'] = 0
        response_data = {}
        response_data['cookId'] = str(cook.id)
        response_data['cookName'] = cook.name
        response_data['cookTelephone'] = cook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    cook = query_cook[0]
    if cook.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif cook.shopId == "":
        cook.shopId = str(shop.id)
        cook.category = None
        cook.save()
        response['code'] = 0
        response_data = {}
        response_data['cookId'] = str(cook.id)
        response_data['cookName'] = cook.name
        response_data['cookTelephone'] = cook.telephone
        response_data['everAttachCategory'] = '0'
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def removeCook(request):
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

    _cookId = request.REQUEST.get('cookId')
    if _cookId == None or _cookId == '':
        response['code'] = -1
        response['errorMsg'] = '获取cookId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _cookId = str(_cookId)
    try:
        cook = Cook.objects.get(id = _cookId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取厨师失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if cook.shopId == str(shop.id):
        orderSkuQuery = OrderSku.objects.filter(cookId = str(str(cook.id))).filter(status = '6')
        if orderSkuQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该厨师正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if cook.category == None:
            cook.shopId = ''
            cook.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '请在品类中将该厨师解绑，然后再删除'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


@csrf_exempt
def verifyServe(request):
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

    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    telephone_match_CM = CM_prog.match(_telephone)
    telephone_match_CU = CU_prog.match(_telephone)
    telephone_match_CT = CT_prog.match(_telephone)

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(_telephone)
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    query_wait_serve = Serve.objects.filter(telephone = _telephone)
    if not query_wait_serve.exists():
        _name = '****'+_telephone[7:11]
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        serve = Serve(telephone = _telephone, name = _name, headImage = _headImage,shopId = str(shop.id))
        serve.save()
        response['code'] = 0
        response_data = {}
        response_data['serveId'] = str(serve.id)
        response_data['serveName'] = serve.name
        response_data['serveTelephone'] = serve.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    serve = query_wait_serve[0]

    if serve.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    elif serve.shopId == "":
        serve.shopId = str(shop.id)
        serve.save()
        response['code'] = 0
        response_data = {}
        response_data['serveId'] = str(serve.id)
        response_data['serveName'] = serve.name
        response_data['serveTelephone'] = serve.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    else:
        response['code'] = -1
        response['errorMsg'] = '该账号已经被其他商家添加'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

@csrf_exempt
def removeServe(request):
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

    _serveId = request.REQUEST.get('serveId')
    if _serveId == None or _serveId == '':
        response['code'] = -1
        response['errorMsg'] = '获取serveId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _serveId = str(_serveId)
    try:
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取serve失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if serve.shopId == str(shop.id):
        orderSkuQuery = OrderSku.objects.filter(serveId = str(serve.id)).filter(status = '8')
        if orderSkuQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该上菜员正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        serve.shopId = ''
        serve.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    else:
        response['code'] = -1
        response['errorMsg'] = '该账号未关联'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
