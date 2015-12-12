#encoding:utf-8
from django.http import HttpResponse
from django.core.cache import cache
import sys,re,json,time,datetime
from pack.models import Shop,ShopWallet,ShopFeedBack,Waiter,Cook,Serve,TransferMoney
from django.views.decorators.csrf import csrf_exempt
from django.contrib.gis import geos
from django.core.exceptions import ObjectDoesNotExist

import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def shopVerifyTelephone(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _telephone = request.REQUEST.get('telephone',18201637776)
    _verify_code = request.REQUEST.get('verifyCode',8888)
    _method = request.REQUEST.get('method')
    _deviceInfo = request.REQUEST.get('deviceInfo')
    _clientID = request.REQUEST.get('clientID','0')
    _deviceToken = request.REQUEST.get('deviceToken','0')

    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _deviceInfo == None or _deviceInfo == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入设备信息'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _deviceToken == None or _deviceToken == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入deviceToken'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入method'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    _telephone = str(_telephone)
    _verify_code = str(_verify_code)
    _clientID = str(_clientID)
    _deviceToken = str(_deviceToken)
    _method = str(_method)

    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    #中国移动：China Mobile
    # 134[0-8],135,136,137,138,139,150,151,157,158,159,182,187,188
    CM_prog = re.compile(r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\d)\d{7}$")
    #CM = r"^1(34[0-8]|(3[5-9]|5[017-9]|8[278])\\d)\\d{7}$"
    #中国联通：China Unicom
    # 130,131,132,152,155,156,185,186
    CU_prog = re.compile(r"^1(3[0-2]|5[256]|8[56])\d{8}$")
    #CU = r"^1(3[0-2]|5[256]|8[56])\\d{8}$"
    # 中国电信：China Telecom
    # 133,1349,153,180,189
    CT_prog = re.compile(r"^1((33|53|8[09])[0-9]|349)\d{7}$")
    #CT = r"^1((33|53|8[09])[0-9]|349)\\d{7}$"
    telephone_match_CM = CM_prog.match(str(_telephone))
    telephone_match_CU = CU_prog.match(str(_telephone))
    telephone_match_CT = CT_prog.match(str(_telephone))

    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    saved_verify_code = cache.get(str(_telephone))
    #print('saved_verify_code:'+str(saved_verify_code))
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _method == '0':
        query_telephone = Waiter.objects.filter(telephone = str(_telephone))
        if not query_telephone.exists():
            _name = '****'+_telephone[7:11]
            _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
            currentTime = time.time()
            currentTime = int(currentTime)
            currentTime = str(currentTime)
            new_waiter = Waiter(telephone=str(_telephone),name = _name, headImage = _headImage,lastLoginTime =
            currentTime,deviceToken = _deviceToken,clientID = _clientID,deviceInfo = _deviceInfo)
            new_waiter.save()
            response['code'] = 0
            response_data = {'type':'0','waiterId':new_waiter.id,'setShopStatus':'0','everSetInfo':'0','shopId':'0'}
            request.session['waiterId'] = new_waiter.id   #new_shop.save()之后，才能在session中设置shopid，未保存之前不知道是多少
            request.session['lastLoginTime'] = currentTime
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        response_data = {}
        response_data['waiterId'] = query_telephone[0].id
        if query_telephone[0].shop == None:
            response_data['setShopStatus'] = '0'
            response_data['shopId'] = '0'
        else:
            response_data['setShopStatus'] = '1'
            response_data['shopId'] = query_telephone[0].shop.id
            request.session['shopId'] = str(query_telephone[0].shop.id)
        response_data['type'] = '0'
        response_data['everSetInfo'] = '1' if query_telephone[0].everSetInfo == True else '0'
        currentTime = time.time()*1000
        currentTime = int(currentTime)
        currentTime = str(currentTime)
        query_telephone.update(clientID = _clientID, deviceToken = _deviceToken,deviceInfo = _deviceInfo,lastLoginTime = currentTime)
        request.session['waiterId'] = query_telephone[0].id
        request.session['lastLoginTime'] = currentTime
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '1':
        query_telephone = Cook.objects.filter(telephone = str(_telephone))
        if not query_telephone.exists():
            _name = '****'+_telephone[7:11]
            _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
            currentTime = time.time()
            currentTime = int(currentTime)
            currentTime = str(currentTime)
            new_cook = Cook(telephone=str(_telephone),name = _name, headImage = _headImage,lastLoginTime =
            currentTime,deviceToken = _deviceToken,clientID = _clientID,deviceInfo = _deviceInfo)
            new_cook.save()
            response['code'] = 0
            response_data = {'type':'1','cookId':new_cook.id,'setShopStatus':'0','everSetInfo':'0','shopId':'0'}
            request.session['cookId'] = new_cook.id   #new_shop.save()之后，才能在session中设置shopid，未保存之前不知道是多少
            request.session['lastLoginTime'] = currentTime
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        response_data = {}
        response_data['cookId'] = query_telephone[0].id
        if query_telephone[0].shopId == '':
            response_data['setShopStatus'] = '0'
            response_data['shopId'] = '0'
        else:
            response_data['setShopStatus'] = '1'
            response_data['shopId'] = str(query_telephone[0].shopId)
        response_data['type'] = '1'
        response_data['everSetInfo'] = '1' if query_telephone[0].everSetInfo == True else '0'
        currentTime = time.time()*1000
        currentTime = int(currentTime)
        currentTime = str(currentTime)
        query_telephone.update(clientID = _clientID, deviceToken = _deviceToken,deviceInfo = _deviceInfo,lastLoginTime = currentTime)
        request.session['cookId'] = query_telephone[0].id
        request.session['lastLoginTime'] = currentTime
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '2':
        query_telephone = Serve.objects.filter(telephone = str(_telephone))
        if not query_telephone.exists():
            _name = '****'+_telephone[7:11]
            _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
            currentTime = time.time()
            currentTime = int(currentTime)
            currentTime = str(currentTime)
            new_serve = Serve(telephone=str(_telephone),name = _name, headImage = _headImage,lastLoginTime =
            currentTime,deviceToken = _deviceToken,clientID = _clientID,deviceInfo = _deviceInfo)
            new_serve.save()
            response['code'] = 0
            response_data = {'type':'2','serveId':new_serve.id,'setShopStatus':0,'everSetInfo':'0','shopId':'0'}
            request.session['serveId'] = new_serve.id   #new_shop.save()之后，才能在session中设置shopid，未保存之前不知道是多少
            request.session['lastLoginTime'] = currentTime
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        response_data = {}
        response_data['serveId'] = query_telephone[0].id
        if query_telephone[0].shopId == '':
            response_data['setShopStatus'] = '0'
            response_data['shopId'] = '0'
        else:
            response_data['setShopStatus'] = '1'
            response_data['shopId'] = str(query_telephone[0].shopId)
        response_data['type'] = '2'
        response_data['everSetInfo'] = '1' if query_telephone[0].everSetInfo == True else '0'
        currentTime = time.time()*1000
        currentTime = int(currentTime)
        currentTime = str(currentTime)
        query_telephone.update(clientID = _clientID, deviceToken = _deviceToken,deviceInfo = _deviceInfo,lastLoginTime = currentTime)
        request.session['serveId'] = query_telephone[0].id
        request.session['lastLoginTime'] = currentTime
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '3':
        query_telephone = Shop.objects.filter(telephone = str(_telephone))
        if not query_telephone.exists():
            currentTime = time.time()
            currentTime = int(currentTime)
            currentTime = str(currentTime)
            new_shop = Shop(telephone=str(_telephone),setInfoStatus = '0',lastLoginTime = currentTime,deviceToken
            = _deviceToken,clientID = _clientID,deviceInfo = _deviceInfo)
            new_shop.save()
            response['code'] = 0
            response_data = {'type':'3','shopId':new_shop.id,'setInfoStatus':0}
            request.session['shopId'] = new_shop.id   #new_shop.save()之后，才能在session中设置shopid，未保存之前不知道是多少
            request.session['lastLoginTime'] = currentTime
            response['data'] = response_data
            return HttpResponse(json.dumps(response),content_type="application/json")

        response_data = {'type':'3','setInfoStatus':query_telephone[0].setInfoStatus,'shopId':query_telephone[0].id}
        currentTime = time.time()*1000
        currentTime = int(currentTime)
        currentTime = str(currentTime)
        query_telephone.update(lastLoginTime = currentTime,clientID = _clientID, deviceToken = _deviceToken,deviceInfo = _deviceInfo)
        request.session['shopId'] = query_telephone[0].id
        request.session['lastLoginTime'] = currentTime
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def shopInfo(request):
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


    _method = request.REQUEST.get('method')
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = '获取method失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _method = str(_method)

    #if method = 0 , add; method = 1,update; method = 2, query
    if _method == '0':
        _name = request.REQUEST.get('name')
        _headImage = request.REQUEST.get('headImage')
        _type = request.REQUEST.get('type',"0")
        _startTimeStamp = request.REQUEST.get('startTimeStamp','200')
        _endTimeStamp = request.REQUEST.get('endTimeStamp','4000')


        if _name == None or _name == '':
            response['code'] = -1
            response['errorMsg'] = '请输入店铺名字'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _type == None or _type == '':
            response['code'] = -1
            response['errorMsg'] = '请选择经营类别'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _headImage == None or _headImage == '':
            _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        if _startTimeStamp == None or _startTimeStamp == '':
            response['code'] = -1
            response['errorMsg'] = '请添加开始时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _endTimeStamp == None or _endTimeStamp == '':
            response['code'] = -1
            response['errorMsg'] = '请添加结束时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        _startTimeStamp = int(_startTimeStamp)
        _endTimeStamp = int(_endTimeStamp)
        if _startTimeStamp > _endTimeStamp:
            response['code'] = -1
            response['errorMsg'] = '开始时间应该小于结束时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _startTimeStamp > 1440*60 or _endTimeStamp > 1440*60:
            response['code'] = -1
            response['errorMsg'] = '营业时间错误'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _startTimeStamp+30*60 > _endTimeStamp:
                response['code'] = -1
                response['errorMsg'] = '营业时间间隔至少半个小时'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        _type = str(_type)
        if (_type == u'快餐'):
            _type = '0'
        elif (_type ==u'炒菜'):
            _type = '1'
        elif (_type ==u'火锅'):
            _type = '2'
        elif (_type ==u'咖啡'):
            _type = '3'
        else:
            _type = '10'

        shop.name = _name
        shop.shopType = _type
        shop.headImage = _headImage
        shop.startTimeStamp = _startTimeStamp
        shop.endTimeStamp = _endTimeStamp
        shop.setInfoStatus = "1"
        shop.save()

        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _method == '1':
        _name = request.REQUEST.get('name')
        _type = request.REQUEST.get('type','0')
        _headImage = request.REQUEST.get('headImage')
        _startTimeStamp = request.REQUEST.get('startTimeStamp','200')
        _endTimeStamp = request.REQUEST.get('endTimeStamp','4000')


        if _name == None or _name == '':
            response['code'] = -1
            response['errorMsg'] = '请输入店铺名字'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _type == None or _type == '':
            response['code'] = -1
            response['errorMsg'] = '请选择经营类别'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _headImage == None or _headImage == '':
            _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
        if _startTimeStamp == None or _startTimeStamp == '':
            response['code'] = -1
            response['errorMsg'] = '请添加开始时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _endTimeStamp == None or _endTimeStamp == '':
            response['code'] = -1
            response['errorMsg'] = '请添加结束时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        _startTimeStamp = int(_startTimeStamp)
        _endTimeStamp = int(_endTimeStamp)
        if _startTimeStamp > _endTimeStamp:
            response['code'] = -1
            response['errorMsg'] = '开始时间应该小于结束时间'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _startTimeStamp > 1440*60 or _endTimeStamp > 1440*60:
            response['code'] = -1
            response['errorMsg'] = '营业时间错误'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _startTimeStamp+30*60 > _endTimeStamp:
                response['code'] = -1
                response['errorMsg'] = '营业时间间隔至少半个小时'
                return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        _type = str(_type)
        if (_type == u'快餐'):
            _type = '0'
        elif (_type ==u'炒菜'):
            _type = '1'
        elif (_type ==u'火锅'):
            _type = '2'
        elif (_type ==u'咖啡'):
            _type = '3'
        else:
            _type = '10'

        shop.name = _name
        shop.shopType = _type
        shop.headImage = _headImage
        shop.startTimeStamp = _startTimeStamp
        shop.endTimeStamp = _endTimeStamp
        shop.save()

        response['code'] = 0
        response_data = {}
        __type = shop.shopType
        if (__type == '0'):
            response_data['type'] = u'快餐'.encode('utf-8')
        elif (__type == '1'):
            response_data['type'] = u'炒菜'.encode('utf-8')
        elif (__type == '2'):
            response_data['type'] = u'火锅'.encode('utf-8')
        elif (__type == '3'):
            response_data['type'] = u'咖啡'.encode('utf-8')
        else:
            response_data['type'] = u'其它'.encode('utf-8')
        response_data['name'] = shop.name.encode('utf-8')
        response_data['telephone'] = shop.telephone
        response_data['headImage'] = shop.headImage
        response_data['startTimeStamp'] = str(shop.startTimeStamp)
        response_data['endTimeStamp'] = str(shop.endTimeStamp)
        response_data['isServiceOn'] = '1' if shop.isServiceOn == True else'0'
        response_data['serveDispatchUnit'] = shop.serveDispatchUnit
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        response['code'] = 0
        response_data = {}
        __type = shop.shopType
        if (__type == '0'):
            response_data['type'] = u'快餐'.encode('utf-8')
        elif (__type == '1'):
            response_data['type'] = u'炒菜'.encode('utf-8')
        elif (__type == '2'):
            response_data['type'] = u'火锅'.encode('utf-8')
        elif (__type == '3'):
            response_data['type'] = u'咖啡'.encode('utf-8')
        else:
            response_data['type'] = u'其它'.encode('utf-8')
        response_data['name'] = shop.name.encode('utf-8')
        response_data['telephone'] = shop.telephone
        response_data['headImage'] = shop.headImage
        response_data['startTimeStamp'] = str(shop.startTimeStamp)
        response_data['endTimeStamp'] = str(shop.endTimeStamp)
        response_data['isServiceOn'] = '1' if shop.isServiceOn == True else'0'
        response_data['serveDispatchUnit'] = shop.serveDispatchUnit
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")






@csrf_exempt
def shopAddressInfo(request):
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


    _method = request.REQUEST.get('method')
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = '获取method失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _method = str(_method)

    #if method = 0 , add; method = 1,update; method = 2, query
    if _method == '0':

        _province = request.REQUEST.get('province','')
        _city = request.REQUEST.get('city','')
        _district = request.REQUEST.get('district','')
        _addressDetail = request.REQUEST.get('addressDetail','')
        _longitude = request.REQUEST.get('longitude')
        _latitude = request.REQUEST.get('latitude')


        if _province == None or _province == '':
            response['code'] = -1
            response['errorMsg'] = '请输入省份'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _city == None or _city == '':
            response['code'] = -1
            response['errorMsg'] = '请输入城市'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _district == None or _district == '':
            response['code'] = -1
            response['errorMsg'] = '请输入地区'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _addressDetail == None or _addressDetail == '':
            response['code'] = -1
            response['errorMsg'] = '请输入详细地址'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _longitude == None or _longitude == '':
            response['code'] = -1
            response['errorMsg'] = '请输入经度'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _latitude == None or _latitude == '':
            response['code'] = -1
            response['errorMsg'] = '请输入纬度'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        point = "POINT(%s %s)" % (float(_longitude), float(_latitude))
        shop.province = _province
        shop.city = _city
        shop.district = _district
        shop.addressDetail = _addressDetail
        shop.location = geos.fromstr(point)
        shop.setInfoStatus = '1'
        shop.save()

        response['code'] = 0
        response['data'] = {'type':'3','setInfoStatus':shop.setInfoStatus,'shopId':shop.id}
        return HttpResponse(json.dumps(response),content_type="application/json")
    elif _method == '1':
        _province = request.REQUEST.get('province','')
        _city = request.REQUEST.get('city','')
        _district = request.REQUEST.get('district','')
        _addressDetail = request.REQUEST.get('addressDetail','')
        _longitude = request.REQUEST.get('longitude')
        _latitude = request.REQUEST.get('latitude')

        if _province == None or _province == '':
            response['code'] = -1
            response['errorMsg'] = '请输入省份'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _city == None or _city == '':
            response['code'] = -1
            response['errorMsg'] = '请输入城市'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _district == None or _district == '':
            response['code'] = -1
            response['errorMsg'] = '请输入地区'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _addressDetail == None or _addressDetail == '':
            response['code'] = -1
            response['errorMsg'] = '请输入详细地址'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _longitude == None or _longitude == '':
            response['code'] = -1
            response['errorMsg'] = '请输入经度'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _latitude == None or _latitude == '':
            response['code'] = -1
            response['errorMsg'] = '请输入纬度'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        point = "POINT(%s %s)" % (float(_longitude), float(_latitude))
        shop.province = _province
        shop.city = _city
        shop.district = _district
        shop.addressDetail = _addressDetail
        shop.location = geos.fromstr(point)
        shop.save()

        response['code'] = 0
        response_data = {}
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        response_data = {}
        logger.info(shop.location)
        _location = shop.location
        if _location != None:
            response_data['longitude'] = shop.location.x
            response_data['latitude'] = shop.location.y
        else:
            response_data['longitude'] = 0
            response_data['latitude'] = 0
        response_data['province'] = shop.province
        response_data['city'] = shop.city
        response_data['district'] = shop.district
        response_data['addressDetail'] = shop.addressDetail
        response['code'] = 0
        response['data'] = response_data
        logger.info(response_data)
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def getShopAccountInfo(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    response_data = {}
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
    response_data['moneyLeft'] = str(shop.shopWallet.moneyLeft)
    response_data['moneyTotal'] = str(shop.shopWallet.moneyTotal)
    response_data['moneyTotalOnPlatform'] = str(shop.shopWallet.moneyTotalOnPlatform)
    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def shopWalletInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    response_data = {}
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
    _method = request.REQUEST.get('method')
    if _method == None or _method == '':
        response['code'] = -1
        response['errorMsg'] = '获取method失败'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _method = str(_method)


    if _method == '0':
        _cardNumber = request.REQUEST.get('cardNumber')
        _realName = request.REQUEST.get('realName')
        _cardTypeDesc = request.REQUEST.get('cardTypeDesc')
        
        if _cardNumber == None or _cardNumber == '':
            response['code'] = -1
            response['errorMsg'] = '请填写账户号码'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _realName == None or _realName == '':
            response['code'] = -1
            response['errorMsg'] = '请填写真实姓名'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _cardTypeDesc == None or _cardTypeDesc == '':
            response['code'] = -1
            response['errorMsg'] = '请选择账户类型'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        _cardNumber = str(_cardNumber)
        _realName = str(_realName)
        _cardType = u'0'
        _cardTypeDesc = str(_cardTypeDesc)
        if (_cardTypeDesc == u'银行卡账户'):
            _cardType = u'0'
        elif (_cardTypeDesc ==u'支付宝账户'):
            _cardType = u'1'

        shopWallet = ShopWallet(realName = _realName, cardNumber = _cardNumber, cardType = _cardType)
        shopWallet.save()
        shop.shopwallet = shopWallet
        shop.setInfoStatus = '2'
        shop.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")

    elif _method == '1':
        _cardNumber = request.REQUEST.get('cardNumber')
        _realName = request.REQUEST.get('realName')
        _cardTypeDesc = request.REQUEST.get('cardTypeDesc')
        if _cardNumber == None or _cardNumber == '':
            response['code'] = -1
            response['errorMsg'] = '请填写账户号码'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _realName == None or _realName == '':
            response['code'] = -1
            response['errorMsg'] = '请填写真实姓名'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        if _cardTypeDesc == None or _cardTypeDesc == '':
            response['code'] = -1
            response['errorMsg'] = '请选择账户类型'
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
        _cardNumber = str(_cardNumber)
        _realName = str(_realName)
        _cardTypeDesc = str(_cardTypeDesc)
        _cardType = u'0'
        if (_cardTypeDesc == u'银行卡账户'):
            _cardType = u'0'
        elif (_cardTypeDesc ==u'支付宝账户'):
            _cardType = u'1'
        shopWallet = shop.shopwallet
        shopWallet.realName = _realName
        shopWallet.cardNumber = _cardNumber
        shopWallet.cardType = _cardType
        shopWallet.save()
        response['code'] = 0
        return HttpResponse(json.dumps(response),content_type="application/json")

    if _method == '2':
        shopWallet = shop.shopwallet
        response_data['realName'] = shopWallet.realName
        response_data['cardNumber'] = shopWallet.cardNumber
        response_data['cardType'] = shopWallet.cardType
        response['code'] = 0
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    response['code'] = -1
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def startService(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    print('shopId : '+str(_shopId))

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

    if shop.category_set.count() == 0:
        response['code'] = -1
        response['errorMsg'] = '请先设置商品，然后再开启服务'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if shop.table_set.count() == 0:
        response['code'] = -1
        response['errorMsg'] = '请先设置餐桌信息，然后再开启服务'
        return HttpResponse(json.dumps(response),content_type="application/json")
    if shop.waiter_set.count() == 0:
        response['code'] = -1
        response['errorMsg'] = '请先设置前台服务员，然后再开启服务'
        return HttpResponse(json.dumps(response),content_type="application/json")
    # if shop.cook_set.count() == 0:
    #     response['code'] = -1
    #     response['errorMsg'] = '请先设置厨师，然后再开启服务'
    #     return HttpResponse(json.dumps(response),content_type="application/json")
    # if shop.serve_set.count() == 0:
    #     response['code'] = -1
    #     response['errorMsg'] = '请先设置上菜员，然后再开启服务'
        return HttpResponse(json.dumps(response),content_type="application/json")
    shop.isServiceOn = True
    try:
        shop.save()
    except Exception,e:
        response['code'] = -1
        response['errorMsg'] = '开启服务失败，请稍后再试'
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def closeService(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _shopId = request.session.get('shopId')
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    print('shopId : '+str(_shopId))

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
    shop.isServiceOn = False
    try:
        shop.save()
    except Exception,e:
        response['code'] = -1
        response['errorMsg'] = '关闭服务失败，请稍后再试'
        return HttpResponse(json.dumps(response),content_type="application/json")
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def shopFeedback(request):
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

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    shopFeedback = ShopFeedBack(shop = shop, msg = _msg, date = datetime.datetime.now())
    shopFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def shopUpdateClientID(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ''
    _shopId = request.session.get('shopId')
    logger.info(_shopId)
    if not _shopId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
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

    if shop.clientID != _clientID:
        shop.clientID = _clientID
        shop.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
