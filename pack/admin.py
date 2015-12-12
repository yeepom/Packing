from django.contrib import admin
from pack.models import User,ShopWallet,Shop,Category,Waiter,Cook,Serve
from pack.models import Sku,Table,Order,OrderSku,OrderSkuBackup,OrderRecord,ShopEvaluate
from pack.models import TransferMoney,ShopFeedBack,WaiterFeedBack,CookFeedBack,ServeFeedBack,UserFeedBack
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','telephone','headImage', 'name','lastLoginTime','clientID','deviceToken','deviceInfo')
admin.site.register(User,UserAdmin)

class ShopWalletAdmin(admin.ModelAdmin):
    list_display = ('id','realName','cardNumber','cardType','moneyLeft','moneyTotal','moneyTotalOnPlatform')
admin.site.register(ShopWallet,ShopWalletAdmin)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','setInfoStatus','shopwallet','telephone','serveDispatchUnit','name','headImage',
                   'shopType','desc','isServiceOn','startTimeStamp','endTimeStamp','star',
                   'location','province','city','district','addressDetail','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')

admin.site.register(Shop,ShopAdmin)

class WaiterAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shop','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Waiter,WaiterAdmin)

class CookAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','category','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Cook,CookAdmin)

class ServeAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Serve,ServeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','categoryName','shop','dispatchUnit')

admin.site.register(Category,CategoryAdmin)

class SkuAdmin(admin.ModelAdmin):
    list_display = ('id','name','desc', 'price','size','category','img','isValid')

admin.site.register(Sku,SkuAdmin)


class TableAdmin(admin.ModelAdmin):
    list_display = ('id','shop','number','isValid','peopleNumber','status','userId','waiterId')

admin.site.register(Table,TableAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','userId','shopId', 'tableId','tableNumber','waiterId','waiterName',
                    'status','priceTotal','note','thirdChargeNO','date')

admin.site.register(Order,OrderAdmin)

class OrderSkuAdmin(admin.ModelAdmin):
    list_display = ('id','order','categoryId','tableId','tableNumber','skuId','skuName','skuPrice', 'skuSizeName',
                    'skuQuantity','status','cookId','cookName','serveId','serveName')

admin.site.register(OrderSku,OrderSkuAdmin)


class OrderSkuBackupAdmin(admin.ModelAdmin):
    list_display = ('id','orderId','orderSkuId','categoryId','tableId','tableNumber','skuId','skuName','skuPrice',
                    'skuSizeName',
'skuQuantity','status','cookId','cookName','serveId','serveName')

admin.site.register(OrderSkuBackup,OrderSkuBackupAdmin)

class OrderRecordAdmin(admin.ModelAdmin):
    list_display = ('id','order','record','date')

admin.site.register(OrderRecord,OrderRecordAdmin)

class ShopEvaluateAdmin(admin.ModelAdmin):
    list_display = ('id','user','shop','star','date')
admin.site.register(ShopEvaluate,ShopEvaluateAdmin)

class TransferMoneyAdmin(admin.ModelAdmin):
    list_display = ('id','shop','total','startDateString','endDateString','date')
admin.site.register(TransferMoney,TransferMoneyAdmin)

class ShopFeedBackAdmin(admin.ModelAdmin):
    list_display = ('shop','msg')

admin.site.register(ShopFeedBack,ShopFeedBackAdmin)

class WaiterFeedBackAdmin(admin.ModelAdmin):
    list_display = ('waiter','msg')

admin.site.register(WaiterFeedBack,WaiterFeedBackAdmin)

class CookFeedBackAdmin(admin.ModelAdmin):
    list_display = ('cook','msg')

admin.site.register(CookFeedBack,CookFeedBackAdmin)

class ServeFeedBackAdmin(admin.ModelAdmin):
    list_display = ('serve','msg')

admin.site.register(ServeFeedBack,ServeFeedBackAdmin)

class UserFeedBackAdmin(admin.ModelAdmin):
    list_display = ('user','msg')

admin.site.register(UserFeedBack,UserFeedBackAdmin)

