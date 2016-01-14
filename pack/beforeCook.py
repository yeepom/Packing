#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import BeforeCook,BeforeCookFeedBack,Shop
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def beforeCookAddInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _name = request.REQUEST.get('name')
    _headImage = request.REQUEST.get('headImage')

    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _headImage == None or _headImage == '':
        _headImage = 'http://meiyue.b0.upaiyun.com/head/1_head.jpg'
    _name = str(_name)
    _headImage = str(_headImage)

    if  beforeCook.everSetInfo == True:
        response['code'] = -1
        response['errorMsg'] = '已经设置过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    beforeCook.name = _name
    beforeCook.headImage = _headImage
    beforeCook.everSetInfo = True
    beforeCook.save()
    response['code'] = 0
    response['data'] = {'type':'3','beforeCookId':str(beforeCook .id)}
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def beforeCookGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['beforeCookName'] = beforeCook.name.encode('utf-8')
    response_data['beforeCookTelephone'] = beforeCook.telephone
    response_data['beforeCookHeadImage'] = beforeCook.headImage
    if beforeCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(beforeCook.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def beforeCookAlterInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')
    _headImage = request.REQUEST.get('headImage')



    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    _name = str(_name)
    _headImage = str(_headImage)


    beforeCook.name = _name
    beforeCook.headImage = _headImage
    beforeCook.save()

    response['code'] = 0
    response_data = {}
    response_data['beforeCookName'] = beforeCook.name.encode('utf-8')
    response_data['beforeCookTelephone'] = beforeCook.telephone
    response_data['beforeCookHeadImage'] = beforeCook.headImage
    if beforeCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(beforeCook.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterBeforeCookName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')


    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    beforeCook.name = _name
    beforeCook.save()

    response['code'] = 0
    response_data = {}
    response_data['beforeCookName'] = beforeCook.name.encode('utf-8')
    response_data['beforeCookTelephone'] = beforeCook.telephone
    response_data['beforeCookHeadImage'] = beforeCook.headImage
    if beforeCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(beforeCook.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterBeforeCookHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    beforeCook.headImage = _headImage
    beforeCook.save()

    response['code'] = 0
    response_data = {}
    response_data['beforeCookName'] = beforeCook.name.encode('utf-8')
    response_data['beforeCookTelephone'] = beforeCook.telephone
    response_data['beforeCookHeadImage'] = beforeCook.headImage
    if beforeCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(beforeCook.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shoptelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def beforeCookFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    beforeCookFeedback = BeforeCookFeedBack(beforeCook = beforeCook, msg = _msg, date =datetime.datetime.now())
    beforeCookFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def beforeCookUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _beforeCookId = request.session.get('beforeCookId')
    if not _beforeCookId:
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
        beforeCook = BeforeCook.objects.get(id = _beforeCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != beforeCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if beforeCook.clientID != _clientID:
        beforeCook.clientID = _clientID
        beforeCook.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
