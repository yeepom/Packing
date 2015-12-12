# encoding:utf-8
from __future__ import absolute_import
import time
from celery.task import task
from pack.pack_push_2_user import pushMessageToSingle
from pack.messageNotify import notify
from pack.models import Order,OrderSku,OrderSkuBackup
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

def syncOrderSkuToCook(orderId):
    logger = logging.getLogger('Pack.app')
    logger.info('syncOrderSku')
    logger.info(orderId)
    orderId = str(orderId)
    try:
        order = Order.objects.select_related().get(id = orderId)
    except ObjectDoesNotExist:
        logger.info('order did not exists')
        return
    logger.info(order)
    orderSkus = order.ordersku_set.filter(everSync = False)
    _orderSkuBackupList = []
    for orderSku in orderSkus:
        _orderSkuBackupList.append(OrderSkuBackup(orderId = orderSku.order.id,orderSkuId = orderSku.id,
            shopId = orderSku.shopId,categoryId =orderSku.categoryId,tableId = orderSku.tableId,
            tableNumber = orderSku.tableNumber,skuId = orderSku.skuId,skuName = orderSku.skuName,
            skuPrice = orderSku.skuPrice,skuSizeName = orderSku.skuSizeName,skuQuantity =orderSku.skuQuantity,
            status = orderSku.status))
    OrderSkuBackup.objects.bulk_create(_orderSkuBackupList)
    orderSkus.update(everSync = True)
    logger.info('-------')

@app.task()

def cookSyncOrderSku(cookId,cookName,status,orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info('cookSyncOrderSku')
    logger.info(orderSkuIdList)
    cookId = str(cookId)
    cookName = str(cookName)
    for orderSkuId in orderSkuIdList:
        try:
            orderSku = OrderSku.objects.select_related().get(id = orderSkuId)
        except ObjectDoesNotExist:
            logger.info('order did not exists')
            break
        orderSku.status = status
        orderSku.cookId = cookId
        orderSku.cookName = cookName
        orderSku.save()

@app.task()

def serveSyncOrderSku(serveId,serveName,status,orderSkuIdList):
    logger = logging.getLogger('Pack.app')
    logger.info('serveSyncOrderSku')
    logger.info(orderSkuIdList)
    serveId = str(serveId)
    serveName = str(serveName)
    for orderSkuId in orderSkuIdList:
        try:
            orderSku = OrderSku.objects.select_related().get(id = orderSkuId)
        except ObjectDoesNotExist:
            logger.info('order did not exists')
            break
        orderSku.status = status
        orderSku.serveId = serveId
        orderSku.serveName = serveName
        orderSku.save()
