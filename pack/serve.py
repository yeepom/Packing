#encoding:utf-8
from django.http import HttpResponse
import sys,json,datetime
from pack.models import Serve,ServeFeedBack,Shop
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import logging

reload(sys)
sys.setdefaultencoding('utf8')

@csrf_exempt
def serveAddInfo(request):
    logger = logging.getLogger('Pack.app')
    logger.info(request)
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
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

    if  serve.everSetInfo == True:
        response['code'] = -1
        response['errorMsg'] = '已经设置过'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    serve.name = _name
    serve.headImage = _headImage
    serve.everSetInfo = True
    serve.save()
    response['code'] = 0
    response['data'] = {'type':'2','cookId':str(serve.id)}
    return HttpResponse(json.dumps(response),content_type="application/json")

@csrf_exempt
def serveGetInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    response['code'] = 0
    response_data = {}
    response_data['serveName'] = serve.name.encode('utf-8')
    response_data['serveTelephone'] = serve.telephone
    response_data['serveHeadImage'] = serve.headImage
    if serve.shopId == '':
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        try:
            shop = Shop.objects.get(id = str(serve.shopId))
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
def serveAlterInfo(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
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

    serve.name = _name
    serve.headImage = _headImage
    serve.save()

    response['code'] = 0
    response_data = {}
    response_data['serveName'] = serve.name.encode('utf-8')
    response_data['serveTelephone'] = serve.telephone
    response_data['serveHeadImage'] = serve.headImage
    if serve.shopId == '':
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(serve.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shopTelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterServeName(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _name = request.REQUEST.get('name')


    if _name == None or _name == '':
        response['code'] = -1
        response['errorMsg'] = '请输入店铺名字'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    serve.name = _name
    serve.save()

    response['code'] = 0
    response_data = {}
    response_data['serveName'] = serve.name.encode('utf-8')
    response_data['serveTelephone'] = serve.telephone
    response_data['serveHeadImage'] = serve.headImage
    if serve.shopId == '':
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")

    else:
        try:
            shop = Shop.objects.get(id = str(serve.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shopTelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")


@csrf_exempt
def alterServeHeadImage(request):
    logger = logging.getLogger('Pack.app')
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _headImage = request.REQUEST.get('headImage')

    if _headImage == None or _headImage == '':
        response['code'] = -1
        response['errorMsg'] = '请输入headImage'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")


    serve.headImage = _headImage
    serve.save()

    response['code'] = 0
    response_data = {}
    response_data['serveName'] = serve.name.encode('utf-8')
    response_data['serveTelephone'] = serve.telephone
    response_data['serveHeadImage'] = serve.headImage
    if serve.shopId == '':
        # response_shopInfo = {}
        # response_shopInfo['shopId'] = ''
        # response_shopInfo['shopName'] = ''
        # response_shopInfo['shoptelephone'] = ''
        # response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")
    else:
        try:
            shop = Shop.objects.get(id = str(serve.shopId))
        except ObjectDoesNotExist:
            logger.info('查找失败店铺')
            response['code'] = 0
            return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

        response_shopInfo = {}
        response_shopInfo['shopId'] = str(shop.id)
        response_shopInfo['shopName'] = str(shop.name)
        response_shopInfo['shopTelephone'] = str(shop.telephone)
        response_data['shopInfo'] = response_shopInfo
        response['data'] = response_data
        return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def serveFeedback(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################

    _msg = request.REQUEST.get('msg')
    if _msg == None or _msg == '':
        response['code'] = -1
        response['errorMsg'] = '请输入改进意见'
        return HttpResponse(json.dumps(response),content_type="application/json")
    serveFeedback = ServeFeedBack(serve = serve, msg = _msg, date = datetime.datetime.now())
    serveFeedback.save()
    response['code'] = 0
    return HttpResponse(json.dumps(response),content_type="application/json")



@csrf_exempt
def serveUpdateClientID(request):
    response = {}
    response['data'] = {}
    response['errorMsg'] = ""
    _serveId = request.session.get('serveId')
    if not _serveId:
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
        serve = Serve.objects.get(id = _serveId)
    except ObjectDoesNotExist:
        response['code'] = 1
        response['errorMsg'] = '请先登录'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")
    if _lastLoginTime != serve.lastLoginTime:
        response['code'] = 1
        response['errorMsg'] = '上次登录失效，请重新登录'
        return HttpResponse(json.dumps(response),content_type="application/json")
    ####################END#################


    _clientID = request.REQUEST.get('clientID')
    if _clientID == None or _clientID == '':
        response['code'] = -1
        response['errorMsg'] = '请上传clientID'
        return HttpResponse(json.dumps(response,ensure_ascii=False),content_type="application/json")

    if serve.clientID != _clientID:
        serve.clientID = _clientID
        serve.save()
    response['code'] = 0
    response['data'] = {'clientID':_clientID}
    response['errorMsg'] = ''
    return HttpResponse(json.dumps(response),content_type="application/json")
