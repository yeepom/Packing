
#encoding:utf-8
from django.http import HttpResponse
from pack.models import Shop,Waiter,Cook,Serve,Order,OrderSkuBackup
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
import base64,urllib,urllib2,sys,re,json,random,logging
from pack.xmltojson import xmltojson

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
        _waiter['waiterId'] = waiter.id
        _waiter['waiterName'] = waiter.name
        _waiter['waiterTelephone'] = waiter.telephone
        _waiterList.append(_waiter)
    response_data['waiterList'] = _waiterList

    cookQuery = Cook.objects.filter(shopId = str(_shopId)).order_by('-id')
    _cookList = []
    for cook in cookQuery:
        _cook = {}
        _cook['cookId'] = cook.id
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
        _cookList.append(_cook)
    response_data['cookList'] =_cookList

    serveQuery = Serve.objects.filter(shopId = str(_shopId)).order_by('-id')
    _serveList = []
    for serve in serveQuery:
        _serve = {}
        _serve['serveId'] = serve.id
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
        _waiter['waiterId'] = waiter.id
        _waiter['waiterName'] = waiter.name
        _waiter['waiterTelephone'] = waiter.telephone
        _waiterList.append(_waiter)
    response['code'] = 0
    response['data'] = _waiterList
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
        _cook['cookId'] = cook.id
        _cook['cookName'] = cook.name
        _cook['cookTelephone'] = cook.telephone
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

    # response_data = {}
    _serveList = []
    for serve in serveQuery:
        _serve = {}
        _serve['serveId'] = serve.id
        _serve['serveName'] = serve.name
        _serve['serveTelephone'] = serve.telephone
        _serveList.append(_serve)
    # response_data['serveList'] = _serveList
    # response_data['serveDispatchUnit'] = shop.serveDispatchUnit
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

    _telephone = request.REQUEST.get('telephone',18201637776)
    _verify_code = request.REQUEST.get('verifyCode',8888)
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
        response_data['waiterId'] = waiter.id
        response_data['waiterName'] = waiter.name
        response_data['waiterTelephone'] = waiter.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    waiter = query_wait_order[0]
    if waiter.shop == shop:
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    waiter.shop = shop
    waiter.save()
    response['code'] = 0
    response_data = {}
    response_data['waiterId'] = waiter.id
    response_data['waiterName'] = waiter.name
    response_data['waiterTelephone'] = waiter.telephone
    response['data'] = response_data
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
        orderQuery = Order.objects.filter(waiterId = str(waiter.id)).filter(status = '0')
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

    _telephone = request.REQUEST.get('telephone',18201637776)
    _verify_code = request.REQUEST.get('verifyCode',8888)
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
        response_data['cookId'] = cook.id
        response_data['cookName'] = cook.name
        response_data['cookTelephone'] = cook.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    cook = query_cook[0]
    if cook.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    cook.shopId = str(shop.id)
    cook.save()
    response['code'] = 0
    response_data = {}
    response_data['cookId'] = cook.id
    response_data['cookName'] = cook.name
    response_data['cookTelephone'] = cook.telephone
    response['data'] = response_data
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
        response['errorMsg'] = '获取waiterOrerId失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _cookId = str(_cookId)
    try:
        cook = Cook.objects.get(id = _cookId)
    except ObjectDoesNotExist:
        response['code'] = -1
        response['errorMsg'] = '获取waiterOrer失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if cook.shopId == str(shop.id):
        orderSkuBackupQuery = OrderSkuBackup.objects.filter(cookId = str(cook.id)).filter(status = '2')
        if orderSkuBackupQuery.exists():
            response['code'] = -1
            response['errorMsg'] = '该厨师正在忙碌中'
            return HttpResponse(json.dumps(response),content_type="application/json")
        if cook.category == None:
            cook.shopId = ''
            cook.category = None
            cook.save()
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        else:
            cookInCategoryCount = Cook.objects.filter(category = cook.category).count()
            if cookInCategoryCount == 1:
                response['code'] = -1
                response['errorMsg'] = '请在品类中将该厨师解绑，然后可以删除'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
            cook.shopId = ''
            cook.category = None
            cook.save()
            response['code'] = 0
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

    _telephone = request.REQUEST.get('telephone',18201637776)
    _verify_code = request.REQUEST.get('verifyCode',8888)
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
        response_data['serveId'] = serve.id
        response_data['serveName'] = serve.name
        response_data['serveTelephone'] = serve.telephone
        response['data'] = response_data
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    serve = query_wait_serve[0]
    if serve.shopId == str(shop.id):
        response['code'] = -1
        response['errorMsg'] = '该账号已经添加过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    serve.shopId = str(shop.id)
    serve.save()
    response['code'] = 0
    response_data = {}
    response_data['serveId'] = serve.id
    response_data['serveName'] = serve.name
    response_data['serveTelephone'] = serve.telephone
    response['data'] = response_data
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
        orderSkuBackupQuery = OrderSkuBackup.objects.filter(serveId = str(serve.id)).filter(status = '5')
        if orderSkuBackupQuery.exists():
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


@csrf_exempt
def alterServeDispatchUnit(request):
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
    _serveDispatchUnit = request.REQUEST.get('serveDispatchUnit')
    if _serveDispatchUnit == None or _serveDispatchUnit == '':
        response['code'] = -1
        response['errorMsg'] = '获取serveDispatchUnit失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _serveDispatchUnit.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的数字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _serveDispatchUnit = int(_serveDispatchUnit)

    shop.serveDispatchUnit = _serveDispatchUnit
    shop.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
