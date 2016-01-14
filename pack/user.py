#encoding:utf-8
from django.http import HttpResponse
from django.core.cache import cache
import base64,urllib,urllib2,sys,re,json,random,time
from pack.models import User,UserFeedBack
from django.views.decorators.csrf import csrf_exempt
import logging
from pack.VoiceVerify import voiceVerify
from django.core.exceptions import ObjectDoesNotExist
from pack.xmltojson import xmltojson

reload(sys)
sys.setdefaultencoding('utf-8')

@csrf_exempt
def sendVerifyCode(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _telephone = request.REQUEST.get('telephone')
    _method = request.REQUEST.get('method','0')
    #method为0，短信验证码，为1，语音验证码.
    #print('get the telephone with POST :'+_telephone)
    if _telephone == None:
        response['code'] = -1
        response['errorMsg'] = '请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone == '':
        response['code'] = -1
        response['errorMsg'] = '请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    # 手机号码:
    # 13[0-9], 14[5,7], 15[0, 1, 2, 3, 5, 6, 7, 8, 9], 17[6, 7, 8], 18[0-9], 170[0-9]
    # 移动号段: 134,135,136,137,138,139,150,151,152,157,158,159,182,183,184,187,188,147,178,1705
    # 联通号段: 130,131,132,155,156,185,186,145,176,1709
    # 电信号段: 133,153,180,181,189,177,1700

    MOBILE_prog = re.compile(r"^1(3[0-9]|4[57]|5[0-35-9]|8[0-9]|70)\d{8}$")

    # 中国移动：China Mobile
    # 134,135,136,137,138,139,150,151,152,157,158,159,182,183,184,187,188,147,178,1705

    CM_prog = re.compile(r"(^1(3[4-9]|4[7]|5[0-27-9]|7[8]|8[2-478])\d{8}$)|(^1705\d{7}$)")


    # 中国联通：China Unicom
    # 130,131,132,155,156,185,186,145,176,1709

    CU_prog = re.compile(r"(^1(3[0-2]|4[5]|5[56]|7[6]|8[56])\d{8}$)|(^1709\d{7}$)")

    # 中国电信：China Telecom
    # 133,153,180,181,189,177,1700

    CT_prog = re.compile(r"(^1(33|53|77|8[019])\d{8}$)|(^1700\d{7}$)")

    telephone_match_MOBILE = MOBILE_prog.match(str(_telephone))
    telephone_match_CM = CM_prog.match(str(_telephone))
    print telephone_match_CM
    telephone_match_CU = CU_prog.match(str(_telephone))
    telephone_match_CT = CT_prog.match(str(_telephone))
    if not telephone_match_MOBILE and not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    saved_verify_code = cache.get(str(_telephone))
    verify_code = 0
    if saved_verify_code:
        verify_code = saved_verify_code
    else:
        verify_code = random.randrange(1000,9999,4)
    if _method =='0':
        base64_password = base64.encodestring('123456')
        content_msg = u'【后厨帮】登陆验证码：'+str(verify_code)+u'，请您妥善保管。'
        params = urllib.urlencode({'action':'send','userid':'695','account':u'快点餐'.encode('utf-8'),'password':'123456',
        'mobile':_telephone,'content':content_msg})
        url_req = "http://115.28.50.135:8888/sms.aspx"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        xmltojsonModel = xmltojson()
        sms_response_json = xmltojsonModel.main(sms_response)
        print(sms_response)
        print sms_response_json
        if sms_response_json['returnstatus'] != 'Success':
            response['code'] = -1
            response['errorMsg'] = sms_response_json['message']
            return HttpResponse(json.dumps(response),content_type="application/json")
        cache.set(str(_telephone),str(verify_code),1800)
        print('send_verify_code:'+cache.get(str(_telephone)))
        response['code'] =  0
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        voice_response = voiceVerify(str(verify_code),2,_telephone,'400-100-111','123.57.134.241/')
        if voice_response['statusCode'] == '000000':
            response['code'] = 0
            return HttpResponse(json.dumps(response),content_type="application/json")
        else:
            response['code'] = -1
            response['errorMsg'] = '请重新发送语音验证码~'
            return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def verifyTelephone(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    logger = logging.getLogger('Pack.app')
    logger.info('-----------------------verifyTelephone')
    _telephone = request.REQUEST.get('telephone')
    _verify_code = request.REQUEST.get('verifyCode')
    _clientID = request.REQUEST.get('clientID')
    _deviceToken = request.REQUEST.get('deviceToken')
    _deviceInfo = request.REQUEST.get('deviceInfo')
    logger.info(str(_telephone))
    cache.set(str(_telephone),str(_verify_code),1800)
    if _telephone == None or _telephone == '':
        response['code'] = -1
        response['errorMsg'] = '请输入手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if  _verify_code == None or _verify_code == '':
        response['code'] = -1
        response['errorMsg'] = '请输入验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _deviceInfo == None or _deviceInfo == '':
        response['code'] = -1
        response['errorMsg'] = u'请输入设备信息'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if len(_telephone) != 11:
        response['code'] = -1
        response['errorMsg'] = '请输入11位手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _telephone.isdigit() == False:
        response['code'] = -1
        response['errorMsg'] = '请输入有效手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if len(_verify_code) != 4:
        response['code'] = -1
        response['errorMsg'] = '请输入4位验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _clientID == None:
        _clientID = ''
    else:
        _clientID = str(_clientID)
    if _deviceToken == None:
        _deviceToken = ''
    else:
        _deviceToken = str(_deviceToken)
    _deviceInfo = str(_deviceInfo)

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
    #print telephone_match_CM
    #print telephone_match_CU
    #print telephone_match_CT
    if not telephone_match_CM and not telephone_match_CT and not telephone_match_CU:
        response['code'] =  -1
        response['errorMsg'] = '请输入有效的手机号'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    saved_verify_code = cache.get(str(_telephone))
    print('saved_verify_code:'+str(saved_verify_code))
    if not saved_verify_code:
        response['code'] = -1
        response['errorMsg'] = '请重新发送验证码'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if saved_verify_code != _verify_code:
        response['code'] = -1
        response['errorMsg'] = '验证码错误，请重新输入'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    query_telephone = User.objects.filter(telephone = str(_telephone))
    if not query_telephone.exists():
        _name = '****'+_telephone[7:11]
        currentTime = time.time()
        currentTime = int(currentTime)
        currentTime = str(currentTime)
        new_user = User(telephone=str(_telephone),name = _name,lastLoginTime = currentTime,clientID =
        _clientID,deviceToken = _deviceToken,deviceInfo = _deviceInfo)

        new_user.save()
        request.session['lastLoginTime'] = currentTime
        response_data = {'userId':new_user.id,'telephone':new_user.telephone,'name':new_user.name,'headImage':new_user.headImage}
        response['code'] = 0
        request.session['userId'] = new_user.id
        response['data'] = response_data
        print('get the new user with id :'+str(new_user.id)+'withtelephone:'+new_user.telephone+'with choice:False')
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    query_telephone.update(clientID=_clientID,deviceToken = _deviceToken,deviceInfo = _deviceInfo)
    currentTime = time.time()*1000
    currentTime = int(currentTime)
    currentTime = str(currentTime)
    logger.info('--------currentTime-----')
    logger.info(currentTime)
    query_telephone.update(lastLoginTime = currentTime)
    request.session['lastLoginTime'] = currentTime
    request.session['userId'] = query_telephone[0].id
    response_data = {'userId':query_telephone[0].id,'telephone':query_telephone[0].telephone,'name':query_telephone[0].name,'headImage':query_telephone[0].headImage}
    response['code'] = 0
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def userGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['name'] = user.name.encode('utf-8')
    response_data['telephone'] = user.telephone
    response_data['headImage'] = user.headImage
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterUserName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')
    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    user.name = _name
    user.save()
    response['code'] = 0
    response_data = {}
    response_data['name'] = user.name.encode('utf-8')
    response_data['telephone'] = user.telephone
    response_data['headImage'] = user.headImage
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterUserHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    user.headImage = _headImage
    user.save()

    response['code'] = 0
    response_data = {}
    response_data['name'] = user.name.encode('utf-8')
    response_data['telephone'] = user.telephone
    response_data['headImage'] = user.headImage
    response['data'] = response_data
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def userFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    ##################JUDGE############
    _lastLoginTime = request.session.get('lastLoginTime')
    if not _lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    try:
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    userFeedback = UserFeedBack(user = user, msg = _msg)
    userFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def userUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _userId = request.session.get('userId')
    if not _userId:
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
        user = User.objects.get(id = _userId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != user.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if user.clientID != _clientID:
        user.clientID = _clientID
        user.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
