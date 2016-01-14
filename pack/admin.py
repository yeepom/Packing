from django.contrib import admin
from pack.models import User,ShopWallet,Shop,Category,Waiter,Cook,Serve,BeforeCook,AfterCook,OrderSeparate
from pack.models import Sku,Table,Order,OrderSku,OrderRecord,ShopEvaluate
from pack.models import TransferMoney,ShopFeedBack,WaiterFeedBack,CookFeedBack,ServeFeedBack,UserFeedBack
from pack.models import OrderSeparateFeedBack,BeforeCookFeedBack,AfterCookFeedBack
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','telephone','headImage', 'name','lastLoginTime','clientID','deviceToken','deviceInfo')
admin.site.register(User,UserAdmin)

class ShopWalletAdmin(admin.ModelAdmin):
    list_display = ('id','realName','cardNumber','cardType','moneyLeft','moneyTotal','moneyTotalOnPlatform')
admin.site.register(ShopWallet,ShopWalletAdmin)

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopwallet','telephone','name','headImage',
                   'shopType','desc','isServiceOn','startTimeStamp','endTimeStamp','star',
                   'location','province','city','district','addressDetail','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')

admin.site.register(Shop,ShopAdmin)

class WaiterAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shop','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Waiter,WaiterAdmin)


class BeforeCookAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','category','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(BeforeCook,BeforeCookAdmin)

class AfterCookAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','category','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(AfterCook,AfterCookAdmin)

class OrderSeparateAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','category','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(OrderSeparate,OrderSeparateAdmin)

class CookAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','category','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Cook,CookAdmin)

class ServeAdmin(admin.ModelAdmin):
    list_display = ('id','everSetInfo','shopId','telephone','name','headImage','clientID','lastLoginTime','clientID',
                    'deviceToken','deviceInfo')
admin.site.register(Serve,ServeAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','categoryName','shop')

admin.site.register(Category,CategoryAdmin)

class SkuAdmin(admin.ModelAdmin):
    list_display = ('id','name','desc', 'price','size','category','img','isValid')

admin.site.register(Sku,SkuAdmin)


class TableAdmin(admin.ModelAdmin):
    list_display = ('id','shop','number','peopleNumber','status','userId','waiterId')

admin.site.register(Table,TableAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','userId','shopId', 'tableId','tableNumber','waiterId','waiterName',
                    'status','priceTotal','note','thirdChargeNO','date')

admin.site.register(Order,OrderAdmin)

class OrderSkuAdmin(admin.ModelAdmin):
    list_display = ('id','order','categoryId','tableId','tableNumber','skuId','skuName','skuPrice', 'skuSizeName',
                    'skuQuantity','status','cookId','cookName','beforeCookId','beforeCookName','orderSeparateId',
                    'orderSeparateName','afterCookId','afterCookName','serveId','serveName')

admin.site.register(OrderSku,OrderSkuAdmin)


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

class OrderSeparateFeedBackAdmin(admin.ModelAdmin):
    list_display = ('orderSeparate','msg')

admin.site.register(OrderSeparateFeedBack,OrderSeparateFeedBackAdmin)

class BeforeCookFeedBackAdmin(admin.ModelAdmin):
    list_display = ('beforeCook','msg')

admin.site.register(BeforeCookFeedBack,BeforeCookFeedBackAdmin)

class AfterCookFeedBackAdmin(admin.ModelAdmin):
    list_display = ('afterCook','msg')

admin.site.register(AfterCookFeedBack,AfterCookFeedBackAdmin)

class ServeFeedBackAdmin(admin.ModelAdmin):
    list_display = ('serve','msg')

admin.site.register(ServeFeedBack,ServeFeedBackAdmin)

class UserFeedBackAdmin(admin.ModelAdmin):
    list_display = ('user','msg')

admin.site.register(UserFeedBack,UserFeedBackAdmin)

