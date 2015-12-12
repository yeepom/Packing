#encoding:utf-8
from django.contrib.gis.db import models as gis_models
from django.db import models
from datetime import datetime

class User(models.Model):
    telephone = models.CharField('电话',max_length=11,unique=True)
    name = models.CharField('昵称',max_length =100)
    headImage = models.CharField('头像',max_length = 100)
    clientID = models.CharField(max_length = 40)
    lastLoginTime = models.CharField('上次登录时间',max_length = 13, default = '0')
    deviceToken = models.CharField('iOS设备号',max_length=64,default = '0')
    deviceInfo = models.CharField('设备名称（iOS、Android）',max_length = 20, default='none')

    def __unicode__(self):
        return ('id:%s,telephone:%s,' % (self.id,self.telephone))
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户列表'

CARD_TYPE_CHOICES=(
    (u'0',u'银行卡'),
    (u'1',u'支付宝账户'),
	)


class ShopWallet(models.Model):
    realName = models.CharField('名字',max_length = 20,default='0')
    cardNumber = models.CharField('卡号',max_length=19,default='0')
    cardType = models.CharField('类型',max_length =1 ,choices = CARD_TYPE_CHOICES,default= '0')
    moneyLeft = models.DecimalField('余额',max_digits = 7, decimal_places = 2, default = 0)
    moneyTotal = models.DecimalField('累计收入',max_digits = 7, decimal_places = 2, default = 0)
    moneyTotalOnPlatform = models.DecimalField('平台累计收入',max_digits = 7, decimal_places = 2, default = 0)


SHOPTYPE_CHOICES=(
    (u'0',u'快餐'),
    (u'1',u'炒菜'),
    (u'2',u'火锅'),
    (u'3',u'咖啡'),
    (u'10',u'其他'),
    )

SET_INFO_CHOICES=(
    (u'0',u'没有设置过基本信息'),
    (u'1',u'没有设置过钱包信息'),
    (u'2',u'设置完毕'),
)

class Shop(models.Model):
    setInfoStatus = models.CharField('设置商家信息状态',choices = SET_INFO_CHOICES,max_length=1,default='0')
    shopwallet = models.OneToOneField(ShopWallet,null=True)
    telephone = models.CharField('电话',max_length=11,unique=True)
    serveDispatchUnit = models.PositiveSmallIntegerField('服务员分配最小单位',default=1)
    name = models.CharField('店铺名',max_length = 50)
    headImage = models.CharField('店铺头像',max_length = 100)
    shopType = models.CharField('商家类型',max_length = 2,choices = SHOPTYPE_CHOICES,default = '0')
    desc = models.CharField('描述',max_length = 200,default='0')
    isServiceOn = models.BooleanField('是否在线服务',default = False)
    startTimeStamp = models.PositiveSmallIntegerField('开始时间戳',max_length=10,default=0)
    endTimeStamp = models.PositiveSmallIntegerField('结束时间戳',max_length=10,default=0)
    star = models.PositiveSmallIntegerField('评价',default=5)
    province = models.CharField('省份',max_length = 20,default='')
    city = models.CharField('城市',max_length = 20,default='')
    district = models.CharField('地区',max_length = 20,default='')
    addressDetail = models.CharField('详细信息',max_length = 100,default='')
    clientID = models.CharField(max_length = 40, default ='000')
    deviceToken = models.CharField('iOS设备号',max_length=64,default = '0')
    deviceInfo = models.CharField('设备名称（iOS、Android）',max_length = 20, default='')
    lastLoginTime = models.CharField('上次登录时间',max_length = 13, default = '0')
    location = gis_models.PointField(u"longitude/latitude",
                                     geography=True, blank=True, null=True)
    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __unicode__(self):
        return ('id:%s,telephone:%s,' % (self.id,self.telephone))
    class Meta:
        verbose_name = '商家'
        verbose_name_plural = '商家列表'

class Category(models.Model):
    shop = models.ForeignKey(Shop)
    categoryName = models.CharField(max_length = 20)
    dispatchUnit = models.PositiveSmallIntegerField('分配最小单位',default=1)
    def __unicode__(self):
        return ('id:%s,name:%s,' % (self.id,self.categoryName))

SHOPPER_STATUS_CHOICES=(
    (u'0',u'空闲'),
    (u'1',u'忙碌'),
    (u'2',u'离线'),
)

class Waiter(models.Model):
    everSetInfo = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop,null=True)
    telephone = models.CharField('电话',max_length=11,unique=True)
    name = models.CharField('店员名',max_length = 50)
    headImage = models.CharField('店员头像',max_length = 100)
    status = models.CharField('状态',max_length=1,choices=SHOPPER_STATUS_CHOICES,default='0')
    clientID = models.CharField(max_length = 40)
    lastLoginTime = models.CharField('上次登录时间',max_length = 13, default = '0')
    deviceToken = models.CharField('iOS设备号',max_length=64,default = '0')
    deviceInfo = models.CharField('设备名称（iOS、Android）',max_length = 20, default='none')
    def __unicode__(self):
        return ('id:%s,telephone:%s,' % (self.id,self.telephone))


class Cook(models.Model):
    everSetInfo = models.BooleanField(default=False)
    shopId = models.CharField('店铺Id',max_length=20,default='')
    category = models.ForeignKey(Category,null=True)
    telephone = models.CharField('电话',max_length=11,unique=True)
    name = models.CharField('店员名',max_length = 50)
    headImage = models.CharField('店员头像',max_length = 100)
    status = models.CharField('状态',max_length=1,choices=SHOPPER_STATUS_CHOICES,default='0')
    clientID = models.CharField(max_length = 40)
    lastLoginTime = models.CharField('上次登录时间',max_length = 13, default = '0')
    deviceToken = models.CharField('iOS设备号',max_length=64,default = '0')
    deviceInfo = models.CharField('设备名称（iOS、Android）',max_length = 20, default='none')
    def __unicode__(self):
        return ('id:%s,telephone:%s,' % (self.id,self.telephone))

class Serve(models.Model):
    everSetInfo = models.BooleanField(default=False)
    shopId = models.CharField('店铺Id',max_length=20,default='')
    telephone = models.CharField('电话',max_length=11,unique=True)
    name = models.CharField('店员名',max_length = 50)
    headImage = models.CharField('店员头像',max_length = 100)
    status = models.CharField('状态',max_length=1,choices=SHOPPER_STATUS_CHOICES,default='0')
    clientID = models.CharField(max_length = 40)
    lastLoginTime = models.CharField('上次登录时间',max_length = 13, default = '0')
    deviceToken = models.CharField('iOS设备号',max_length=64,default = '0')
    deviceInfo = models.CharField('设备名称（iOS、Android）',max_length = 20, default='none')
    def __unicode__(self):
        return ('id:%s,telephone:%s,' % (self.id,self.telephone))


class Sku(models.Model):
    name = models.CharField('名字',max_length = 50)
    desc = models.CharField('描述',max_length = 200)
    #img以“,”为间隔，主图放在第一个img第一个位置
    category = models.ForeignKey(Category)
    img = models.CharField('图像',max_length = 500)
    isValid = models.BooleanField('是否有效',default = True)
    price = models.CharField('价格',max_length=200)
    size = models.CharField('型号',max_length=200,default='常规')

    def __unicode__(self):
        return ('id:%s,name:%s,' % (self.id,self.name))



TABLE_STATUS=(
    (u'0',u'空闲'),#0
    (u'1',u'用户锁定'),#1
    (u'2',u'商家锁定'),#2
    (u'3',u'忙碌'),#3
)


class Table(models.Model):
    shop = models.ForeignKey(Shop)
    number = models.CharField('号码',max_length=100)
    peopleNumber = models.PositiveSmallIntegerField('容纳人数',default=2)
    status = models.CharField('状态',max_length=1,choices=TABLE_STATUS,default='0')
    isValid = models.BooleanField('是否有效',default = True)
    userId = models.CharField('用户id',max_length=20,default='0')
    waiterId = models.CharField('点菜员id',max_length=20,default='0')
    lockDateTime = models.DateTimeField('日期')
    def __unicode__(self):
        return ('id:%s,name:%s,' % (self.id, self.number))


ORDER_STATUS_CHOICES=(
    (u'0',u'处理中'),
	(u'2',u'待付款'),	  #lockTableStyle为1时，无此状态
    (u'4',u'待评价'),  #lockTableStyle为1时，无此状态
	(u'6',u'完成'),
)


class Order(models.Model):
    shopId = models.CharField('店铺Id',max_length=20,default='')
    waiterId = models.CharField('点菜员id',max_length=20,default='0')
    waiterName = models.CharField('点菜员名字',max_length=20,default='')
    userId = models.CharField('用户id',max_length=20,default='')  #userId为空，则没有用户锁定该餐桌
    tableId = models.CharField('餐桌id',max_length=20)
    tableNumber = models.CharField('餐桌号',max_length=100)
    priceTotal = models.DecimalField('总计',max_digits = 8, decimal_places = 2)
    status = models.CharField('状态',max_length = 4, choices = ORDER_STATUS_CHOICES, default='0')
    thirdChargeNO = models.CharField('第三方交易id',max_length=40,default='0')
    note = models.CharField('记录',max_length = 200,default='')
    date = models.DateTimeField('日期')

    def __unicode__(self):
        return ('id:%s' % (self.id))

ORDERSKU_STATUS=(
    (u'0',u'未处理'),#0
    (u'2',u'厨房处理中'),#2
    (u'4',u'厨房已处理'),#4
    (u'5',u'正在上菜'),#5
    (u'6',u'已上菜'),#6
    (u'200',u'取消'),#200
)

class OrderSku(models.Model):
    order = models.ForeignKey(Order)
    shopId = models.CharField('shopId',max_length=20,default='0')
    categoryId = models.CharField('categoryId',max_length=20,default='0')
    tableId = models.CharField('餐桌id',max_length=20)
    tableNumber = models.CharField('餐桌号',max_length=100)
    skuId = models.CharField("skuId",max_length=20,default='1')
    skuName = models.CharField('sku名字',max_length = 50)
    skuPrice = models.DecimalField('单价',max_digits = 6, decimal_places = 2,default=1)
    skuSizeName = models.CharField('型号',max_length = 200)
    skuQuantity = models.PositiveIntegerField('数量',default=0)
    status = models.CharField('状态',max_length=3,default='0',choices=ORDERSKU_STATUS)
    cookId = models.CharField('厨师id',max_length=20,default='')
    cookName = models.CharField('厨师名字',max_length=20,default='')
    serveId = models.CharField('上菜员id',max_length=20,default='')
    serveName = models.CharField('上菜员名字',max_length=20,default='')
    everSync = models.BooleanField(default=False)
    def __unicode__(self):
        return ('id:%s' % (self.id))

class OrderSkuBackup(models.Model):
    orderSkuId = models.CharField('orderSkuId',unique=True,max_length=20,default='')
    orderId = models.CharField('orderId',max_length=20,default='0')
    shopId = models.CharField('shopId',max_length=20,default='0')
    categoryId = models.CharField('categoryId',max_length=20,default='0')
    tableId = models.CharField('餐桌id',max_length=20)
    tableNumber = models.CharField('餐桌号',max_length=100)
    skuId = models.CharField("skuId",max_length=20,default='1')
    skuName = models.CharField('sku名字',max_length = 50)
    skuPrice = models.DecimalField('单价',max_digits = 6, decimal_places = 2,default=1)
    skuSizeName = models.CharField('型号',max_length = 200)
    skuQuantity = models.PositiveIntegerField('数量',default=0)
    status = models.CharField('状态',max_length=3,default='0',choices=ORDERSKU_STATUS)
    cookId = models.CharField('厨师id',max_length=20,default='')
    cookName = models.CharField('厨师名字',max_length=20,default='')
    serveId = models.CharField('上菜员id',max_length=20,default='')
    serveName = models.CharField('上菜员名字',max_length=20,default='')

    def __unicode__(self):
        return ('id:%s' % (self.id))


class OrderRecord(models.Model):
    order = models.ForeignKey(Order)
    record = models.CharField('描述',max_length = 200)
    date = models.DateTimeField('日期')


class ShopEvaluate(models.Model):
    user = models.ForeignKey(User)
    shop = models.ForeignKey(Shop)
    star = models.PositiveSmallIntegerField('评价')
    date = models.DateTimeField('日期')
    def __unicode__(self):
        return ('id:%s' % (self.id))


class TransferMoney(models.Model):
    shop = models.ForeignKey(Shop)
    total = models.DecimalField('金额',max_digits = 8, decimal_places = 2)
    startDateString = models.CharField('开始日期',max_length = 40)
    endDateString = models.CharField('结束日期',max_length = 40)
    date = models.DateTimeField('日期')


class ShopFeedBack(models.Model):
    shop = models.ForeignKey(Shop)
    msg = models.CharField('内容',max_length = 400)
    date = models.DateTimeField(default=datetime.now())

class WaiterFeedBack(models.Model):
    waiter = models.ForeignKey(Waiter)
    msg = models.CharField('内容',max_length = 400)
    date = models.DateTimeField(default=datetime.now())

class CookFeedBack(models.Model):
    cook = models.ForeignKey(Cook)
    msg = models.CharField('内容',max_length = 400)
    date = models.DateTimeField(default=datetime.now())

class ServeFeedBack(models.Model):
    serve = models.ForeignKey(Serve)
    msg = models.CharField('内容',max_length = 400)
    date = models.DateTimeField(default=datetime.now())

class UserFeedBack(models.Model):
    user = models.ForeignKey(User)
    msg = models.CharField('内容',max_length = 400)
    date = models.DateTimeField(default=datetime.now())
