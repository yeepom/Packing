#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import AfterCook,AfterCookFeedBack,Shop
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def afterCookAddInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
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

    if  afterCook.everSetInfo == True:
        response['code'] = -1
        response['errorMsg'] = '已经设置过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    afterCook.name = _name
    afterCook.headImage = _headImage
    afterCook.everSetInfo = True
    afterCook.save()
    response['code'] = 0
    response['data'] = {'type':'5','afterCookId':str(afterCook .id)}
    return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def afterCookGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['afterCookName'] = afterCook.name.encode('utf-8')
    response_data['afterCookTelephone'] = afterCook.telephone
    response_data['afterCookHeadImage'] = afterCook.headImage
    if afterCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(afterCook.shopId))
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
def afterCookAlterInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
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


    afterCook.name = _name
    afterCook.headImage = _headImage
    afterCook.save()

    response['code'] = 0
    response_data = {}
    response_data['afterCookName'] = afterCook.name.encode('utf-8')
    response_data['afterCookTelephone'] = afterCook.telephone
    response_data['afterCookHeadImage'] = afterCook.headImage
    if afterCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(afterCook.shopId))
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
def alterAfterCookName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')


    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    afterCook.name = _name
    afterCook.save()

    response['code'] = 0
    response_data = {}
    response_data['afterCookName'] = afterCook.name.encode('utf-8')
    response_data['afterCookTelephone'] = afterCook.telephone
    response_data['afterCookHeadImage'] = afterCook.headImage
    if afterCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(afterCook.shopId))
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
def alterAfterCookHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    afterCook.headImage = _headImage
    afterCook.save()

    response['code'] = 0
    response_data = {}
    response_data['afterCookName'] = afterCook.name.encode('utf-8')
    response_data['afterCookTelephone'] = afterCook.telephone
    response_data['afterCookHeadImage'] = afterCook.headImage
    if afterCook.shopId == '':
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(afterCook.shopId))
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
def afterCookFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入反馈内容'
        return HttpResponse(json.dumps(response),content_type="application/json")
    afterCookFeedback = AfterCookFeedBack(afterCook = afterCook, msg = _msg, date =datetime.datetime.now())
    afterCookFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def afterCookUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _afterCookId = request.session.get('afterCookId')
    if not _afterCookId:
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
        afterCook = AfterCook.objects.get(id = _afterCookId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != afterCook.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if afterCook.clientID != _clientID:
        afterCook.clientID = _clientID
        afterCook.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
