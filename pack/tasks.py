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
    pushRst = pushMessageToSingle(clientID,type)
    if pushRst['result'] != 'successed_online':
        notify(telephone,type)


@app.task()

def waiterPushMessage(orderId):
    logger = logging.getLogger('Pack.app')
    logger.info("waiterPushMessage")
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

        if orderSku.categoryType == '0' or orderSku.categoryType == '1' or orderSku.categoryType == '2':
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

            payload = '{"method":"pushNewOrderSkusToOrderSeparate"}'
            if(len(orderSeparate.deviceToken and "iOS") == 3):
                pushAPNToShop(orderSeparate.deviceToken,'0',payload)
            else:
                pushMessageToSingle(orderSeparate.clientID,payload)

        elif orderSku.categoryType == '3':
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
            payload = '{"method":"pushNewOrderSkusToServe"}'
            if(len(serve.deviceToken and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,'0',payload)
            else:
                pushMessageToSingle(serve.clientID,payload)
    try:
        shop = Shop.objects.get(id = str(order.shopId))
    except ObjectDoesNotExist:
        logger.info('查找不到shop'+order.shopId)
        return
    payload = '{"method":"pushNewOrdersToSaler"}'
    if(len(shop.deviceToken and "iOS") == 3):
        pushAPNToShop(shop.deviceToken,'0',payload)
    else:
        pushMessageToSingle(shop.clientID,payload)
    logger.info('-------')



@app.task()

def waiterPushMessageWithAddSkus(orderId):
    logger = logging.getLogger('Pack.app')
    logger.info("waiterPushMessage")
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

        if orderSku.categoryType == '0' or orderSku.categoryType == '1' or orderSku.categoryType == '2':
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

            payload = '{"method":"pushNewOrderSkusToOrderSeparate"}'
            if(len(orderSeparate.deviceToken and "iOS") == 3):
                pushAPNToShop(orderSeparate.deviceToken,'0',payload)
            else:
                pushMessageToSingle(orderSeparate.clientID,payload)

        elif orderSku.categoryType == '3':
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
            payload = '{"method":"pushNewOrderSkusToServe"}'
            if(len(serve.deviceToken and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,'0',payload)
            else:
                pushMessageToSingle(serve.clientID,payload)
    try:
        shop = Shop.objects.get(id = str(order.shopId))
    except ObjectDoesNotExist:
        logger.info('查找不到shop'+order.shopId)
        return
    payload = '{"method":"pushNewOrdersToSalerWithAddSkus"}'
    if(len(shop.deviceToken and "iOS") == 3):
        pushAPNToShop(shop.deviceToken,'2',payload)
    else:
        pushMessageToSingle(shop.clientID,payload)
    logger.info('-------')


@app.task()

def waiterPushMessageWithCalcelOrderSkus(orderId):
    logger = logging.getLogger('Pack.app')
    logger.info("waiterPushMessage")
    logger.info(orderId)
    orderId = str(orderId)
    try:
        order = Order.objects.select_related().get(id = orderId)
    except ObjectDoesNotExist:
        logger.info('order did not exists')
        return
    logger.info(order)
    try:
        shop = Shop.objects.get(id = str(order.shopId))
    except ObjectDoesNotExist:
        logger.info('查找不到shop'+order.shopId)
        return
    payload = '{"method":"pushNewOrdersToSalerWithCancelOrderSkus"}'
    if(len(shop.deviceToken and "iOS") == 3):
        pushAPNToShop(shop.deviceToken,'4',payload)
    else:
        pushMessageToSingle(shop.clientID,payload)
    logger.info('-------')



@app.task()

def orderSeparatePushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info("orderSeparatePushMessage")
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
            payload = '{"method":"pushNewOrderSkusToBeforeCook"}'
            if(len(beforeCook.deviceToken and "iOS") == 3):
                pushAPNToShop(beforeCook.deviceToken,'0',payload)
            else:
                pushMessageToSingle(beforeCook.clientID,payload)
        elif orderSku.categoryType == '1' and orderSku.status == '6' and orderSku.afterCookId == '':
            try:
                category = Category.objects.get(id = orderSku.categoryId)
            except ObjectDoesNotExist:
                logger.info('查找不到category'+orderSku.categoryId)
                break
            afterCookCount = category.aftercook_set.count()
            index = int(orderSku.id) % afterCookCount
            afterCook = category.aftercook_set.all()[index]
            orderSku.afterCookId = str(afterCook.id)
            orderSku.afterCookName = afterCook.name
            orderSku.save()
            payload = '{"method":"pushNewOrderSkusToAfterCook"}'
            if(len(afterCook.deviceToken and "iOS") == 3):
                pushAPNToShop(afterCook.deviceToken,'0',payload)
            else:
                pushMessageToSingle(afterCook.clientID,payload)
        elif orderSku.categoryType == '2' and orderSku.status == '8' and orderSku.serveId == '':
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
            payload = '{"method":"pushNewOrderSkusToServe"}'
            if(len(serve.deviceToken and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,'0',payload)
            else:
                pushMessageToSingle(serve.clientID,payload)

    logger.info('-------')


@app.task()

def beforeCookPushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info("beforeCookPushMessage")
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
            payload = '{"method":"pushNewOrderSkusToAfterCook"}'
            if(len(afterCook.deviceToken and "iOS") == 3):
                pushAPNToShop(afterCook.deviceToken,'0',payload)
            else:
                pushMessageToSingle(afterCook.clientID,payload)

    logger.info('-------')


@app.task()

def afterCookPushMessage(orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info("afterCookPushMessage")
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
            payload = '{"method":"pushNewOrderSkusToServe"}'
            if(len(serve.deviceToken and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,'0',payload)
            else:
                pushMessageToSingle(serve.clientID,payload)
        elif orderSku.categoryType == '1' and orderSku.status == '8':
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
            logger.info("index")
            logger.info(index)
            serve = serveQuery[index]
            orderSku.serveId = str(serve.id)
            orderSku.serveName = serve.name
            orderSku.save()
            logger.info("serveId")
            logger.info(orderSku.serveId)
            payload = '{"method":"pushNewOrderSkusToServe"}'
            if(len(serve.deviceToken and "iOS") == 3):
                pushAPNToShop(serve.deviceToken,'0',payload)
            else:
                pushMessageToSingle(serve.clientID,payload)

    logger.info('-------')
