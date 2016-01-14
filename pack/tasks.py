# encoding:utf-8
from __future__ import absolute_import
import time
from celery.task import task
from pack.pack_push_2_shop import pushAPNToShop,pushMessageToSingle
from pack.messageNotify import notify
from pack.models import Order,OrderSku,Category,Shop,Serve
import logging
from django.core.exceptions import ObjectDoesNotExist
from packing.celery import app

@app.task()

def sendMsg(clientID, type, orderId, telephone):
    print("sendMsg")
    pushRst = pushMessageToSingle(clientID,type,orderId)
    if pushRst['result'] != 'successed_online':
        notify(telephone,type)


@app.task()

def waiterPushMessage(orderId):
    logger = logging.getLogger('Pack.app')
    logger.info(orderId)
    orderId = str(orderId)
    try:
        order = Order.objects.select_related().get(id = orderId)
    except ObjectDoesNotExist:
        logger.info('order did not exists')
        return
    logger.info(order)
    orderSkus = order.ordersku_set.filter(status = "0").order_by('categoryId')
    for orderSku in orderSkus:

        if orderSku.categoryType == '0' or orderSku.categoryType == '1':
            try:
                category = Category.objects.get(id = orderSku.categoryId)
            except ObjectDoesNotExist:
                logger.info('查找不到category'+orderSku.categoryId)
                break
            orderSeparateCount = category.orderseparate_set.count()
            index = int(orderSku.id) % orderSeparateCount
            orderSeparate = category.orderseparate_set.all()[index]
            orderSku.orderSeparateId = str(orderSeparate.id)
            orderSku.orderSeparateName = orderSeparate.name
            orderSku.status='2'
            orderSku.save()
            _deviceInfo = orderSeparate.deviceInfo

            payload = '{"method":"pushToOrderSeparate"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(orderSeparate.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(orderSeparate.clientID,payload)

        elif orderSku.categoryType == '2':
            try:
                shop = Shop.objects.get(id = orderSku.shopId)
            except ObjectDoesNotExist:
                logger.info('查找不到shop'+orderSku.shopId)
                break
            serveQuery = Serve.objects.filter(shopId = str(shop.id))
            if not serveQuery.exists:
                logger.info('查找不到serve')
                return
            serveCount = serveQuery.count()
            index = int(orderSku.id) % serveCount
            serve = serveQuery[index]
            orderSku.serveId = str(serve.id)
            orderSku.serveName = serve.name
            orderSku.status = '8'
            orderSku.save()
            _deviceInfo = serve.deviceInfo
            payload = '{"method":"pushToServe"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(serve.clientID,payload)

    logger.info('-------')

@app.task()

def orderSeparatePushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info(orderSkuIdList)
    for orderSkuId in orderSkuIdList:
        try:
            orderSku = OrderSku.objects.get(id = str(orderSkuId))
        except ObjectDoesNotExist:
            logger.info("orderSku not found")
            break
        if orderSku.categoryType == '0' and orderSku.status == '4' and orderSku.beforeCookId == '':
            try:
                category = Category.objects.get(id = orderSku.categoryId)
            except ObjectDoesNotExist:
                logger.info('查找不到category'+orderSku.categoryId)
                break
            beforeCookCount = category.beforecook_set.count()
            index = int(orderSku.id) % beforeCookCount
            beforeCook = category.beforecook_set.all()[index]
            orderSku.beforeCookId = str(beforeCook.id)
            orderSku.beforeCookName = beforeCook.name
            orderSku.save()
            _deviceInfo = beforeCook.deviceInfo
            payload = '{"method":"pushToBeforeCook"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(beforeCook.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(beforeCook.clientID,payload)
        elif orderSku.categoryType == '1' and orderSku.status == '8' and orderSku.serveId == '':
            try:
                shop = Shop.objects.get(id = orderSku.shopId)
            except ObjectDoesNotExist:
                logger.info('查找不到shop'+orderSku.shopId)
                break
            serveQuery = Serve.objects.filter(shopId = str(shop.id))
            if not serveQuery.exists:
                logger.info('查找不到serve')
                return
            serveCount = serveQuery.count()
            index = int(orderSku.id) % serveCount
            serve = serveQuery[index]
            orderSku.serveId = str(serve.id)
            orderSku.serveName = serve.name
            orderSku.save()
            _deviceInfo = serve.deviceInfo
            payload = '{"method":"pushToServe"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(serve.clientID,payload)

    logger.info('-------')


@app.task()

def beforeCookPushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info(orderSkuIdList)
    for orderSkuId in orderSkuIdList:
        try:
            orderSku = OrderSku.objects.get(id = str(orderSkuId))
        except ObjectDoesNotExist:
            logger.info("orderSku not found")
            break
        if orderSku.categoryType == '0' and orderSku.status == '6':
            try:
                shop = Shop.objects.get(id = orderSku.shopId)
            except ObjectDoesNotExist:
                logger.info('查找不到shop'+orderSku.shopId)
                break
            try:
                category = Category.objects.get(id = orderSku.categoryId)
            except ObjectDoesNotExist:
                logger.info('查找不到category'+orderSku.categoryId)
                return
            afterCookCount = category.aftercook_set.count()
            index = int(orderSku.id) % afterCookCount
            afterCook = category.aftercook_set.all()[index]
            orderSku.afterCookId = str(afterCook.id)
            orderSku.afterCookName = afterCook.name
            orderSku.save()
            _deviceInfo = afterCook.deviceInfo
            payload = '{"method":"pushToAfterCook"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(afterCook.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(afterCook.clientID,payload)


    logger.info('-------')


def afterCookPushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info(orderSkuIdList)
    for orderSkuId in orderSkuIdList:
        try:
            orderSku = OrderSku.objects.get(id = str(orderSkuId))
        except ObjectDoesNotExist:
            logger.info("orderSku not found")
            break
        if orderSku.categoryType == '0' and orderSku.status == '8':
            try:
                shop = Shop.objects.get(id = orderSku.shopId)
            except ObjectDoesNotExist:
                logger.info('查找不到shop'+orderSku.shopId)
                break
            serveQuery = Serve.objects.filter(shopId = str(shop.id))
            if not serveQuery.exists:
                logger.info('查找不到serve')
                return
            serveCount = serveQuery.count()
            index = int(orderSku.id) % serveCount
            serve = serveQuery[index]
            orderSku.serveId = str(serve.id)
            orderSku.serveName = serve.name
            orderSku.save()
            _deviceInfo = serve.deviceInfo
            payload = '{"method":"pushToServe"}'
            if(len(_deviceInfo and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,"0",payload)
            elif(len(_deviceInfo and 'Android') == 7):
                pushMessageToSingle(serve.clientID,payload)

    logger.info('-------')
