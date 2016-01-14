
from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'packing.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sendVerifyCode$','pack.user.sendVerifyCode'),
    url(r'^verifyTelephone$','pack.user.verifyTelephone'),
    url(r'^userGetInfo$','pack.user.userGetInfo'),
    url(r'^userFeedback$','pack.user.userFeedback'),
    url(r'^userUpdateClientID$','pack.user.userUpdateClientID'),

    url(r'^getShopsNearby$','pack.user_nearby.getShopsNearby'),
    url(r'^getTablesWithShop$','pack.user_nearby.getTablesWithShop'),
    url(r'^userLockTable$','pack.user_nearby.userLockTable'),
    url(r'^userUnlockTable$','pack.user_nearby.userUnlockTable'),
    url(r'^userGetTableLockDetail$','pack.user_nearby.userGetTableLockDetail'),
    url(r'^checkUserTable$','pack.user_nearby.checkUserTable'),
    url(r'^getShopDetail$','pack.user_nearby.getShopDetail'),

    url(r'^getUserOrders$','pack.user_order.getUserOrders'),
    url(r'^getUserOrderDetail$','pack.user_order.getUserOrderDetail'),

    url(r'^aliPay$','pack.user_pay.aliPay'),
    url(r'^getPayResult$','pack.user_pay.getPayResult'),

    url(r'^shopVerifyTelephone$','pack.shop.shopVerifyTelephone'),
    url(r'^shopInfo$','pack.shop.shopInfo'),
    url(r'^shopAddressInfo$','pack.shop.shopAddressInfo'),
    url(r'^getShopAccountInfo$','pack.shop.getShopAccountInfo'),
    url(r'^shopWalletInfo$','pack.shop.shopWalletInfo'),
    url(r'^startService$','pack.shop.startService'),
    url(r'^closeService$','pack.shop.closeService'),
    url(r'^shopFeedback$','pack.shop.shopFeedback'),
    url(r'^shopUpdateClientID$','pack.shop.shopUpdateClientID'),

    url(r'^getMemberList$','pack.shop_member.getMemberList'),
    url(r'^getWaiterList$','pack.shop_member.getWaiterList'),
    url(r'^getCookList$','pack.shop_member.getCookList'),
    url(r'^getServeList$','pack.shop_member.getServeList'),
    url(r'^getOrderSeparateList$','pack.shop_member.getOrderSeparateList'),
    url(r'^getBeforeCookList$','pack.shop_member.getBeforeCookList'),
    url(r'^getAfterCookList$','pack.shop_member.getAfterCookList'),

    url(r'^verifyWaiter$','pack.shop_member.verifyWaiter'),
    url(r'^verifyCook$','pack.shop_member.verifyCook'),
    url(r'^verifyServe$','pack.shop_member.verifyServe'),
    url(r'^verifyOrderSeparate$','pack.shop_member.verifyOrderSeparate'),
    url(r'^verifyBeforeCook$','pack.shop_member.verifyBeforeCook'),
    url(r'^verifyAfterCook$','pack.shop_member.verifyAfterCook'),
    url(r'^removeWaiter$','pack.shop_member.removeWaiter'),
    url(r'^removeCook$','pack.shop_member.removeCook'),
    url(r'^removeServe$','pack.shop_member.removeServe'),
    url(r'^removeOrderSeparate$','pack.shop_member.removeOrderSeparate'),
    url(r'^removeBeforeCook$','pack.shop_member.removeBeforeCook'),
    url(r'^removeAfterCook$','pack.shop_member.removeAfterCook'),

    url(r'^getCategories$','pack.shop_sku.getCategories'),
    url(r'^addCategory$','pack.shop_sku.addCategory'),
    url(r'^alterCategory$','pack.shop_sku.alterCategory'),
    url(r'^getSkusWithCategory$','pack.shop_sku.getSkusWithCategory'),
    url(r'^skuInfo$','pack.shop_sku.skuInfo'),

    url(r'^addOrderSeparatesToCategory$','pack.shop_sku_order_separate.addOrderSeparatesToCategory'),
    url(r'^getOrderSeparatesInCategory$','pack.shop_sku_order_separate.getOrderSeparatesInCategory'),
    url(r'^getFreeOrderSeparateList$','pack.shop_sku_order_separate.getFreeOrderSeparateList'),
    url(r'^removeOrderSeparateInCategory$','pack.shop_sku_order_separate.removeOrderSeparateInCategory'),

    url(r'^addBeforeCooksToCategory$','pack.shop_sku_beforeCook.addBeforeCooksToCategory'),
    url(r'^getBeforeCooksInCategory$','pack.shop_sku_beforeCook.getBeforeCooksInCategory'),
    url(r'^getFreeBeforeCookList$','pack.shop_sku_beforeCook.getFreeBeforeCookList'),
    url(r'^removeBeforeCookInCategory$','pack.shop_sku_beforeCook.removeBeforeCookInCategory'),


    url(r'^addCooksToCategory$','pack.shop_sku_cook.addCooksToCategory'),
    url(r'^getCooksInCategory$','pack.shop_sku_cook.getCooksInCategory'),
    url(r'^getFreeCookList$','pack.shop_sku_cook.getFreeCookList'),
    url(r'^removeCookInCategory$','pack.shop_sku_cook.removeCookInCategory'),

    url(r'^addAfterCooksToCategory$','pack.shop_sku_afterCook.addAfterCooksToCategory'),
    url(r'^getAfterCooksInCategory$','pack.shop_sku_afterCook.getAfterCooksInCategory'),
    url(r'^getFreeAfterCookList$','pack.shop_sku_afterCook.getFreeAfterCookList'),
    url(r'^removeAfterCookInCategory$','pack.shop_sku_afterCook.removeAfterCookInCategory'),

    url(r'^getTableList$','pack.shop_table.getTableList'),
    url(r'^tableInfo$','pack.shop_table.tableInfo'),
    url(r'^alterTableNumber$','pack.shop_table.alterTableNumber'),
    url(r'^alterTablePeopleNumber$','pack.shop_table.alterTablePeopleNumber'),
    url(r'^resetTableStatus$','pack.shop_table.resetTableStatus'),

    url(r'^getShopOrderListWithTable$','pack.shop_order.getShopOrderListWithTable'),
    url(r'^getShopOrderDetail$','pack.shop_order.getShopOrderDetail'),
    url(r'^getShopDoingOrderList$','pack.shop_order.getShopDoingOrderList'),

    url(r'^waiterAddInfo$','pack.waiter.waiterAddInfo'),
    url(r'^waiterGetInfo$','pack.waiter.waiterGetInfo'),
    url(r'^waiterAlterInfo$','pack.waiter.waiterAlterInfo'),
    url(r'^alterWaiterName$','pack.waiter.alterWaiterName'),
    url(r'^alterWaiterHeadImage$','pack.waiter.alterWaiterHeadImage'),
    url(r'^waiterFeedback$','pack.waiter.waiterFeedback'),
    url(r'^waiterUpdateClientID$','pack.waiter.waiterUpdateClientID'),

    url(r'^waiterGetShopSkus$','pack.waiter_sku.waiterGetShopSkus'),

    url(r'^waiterGetTableList$','pack.waiter_table.waiterGetTableList'),
    url(r'^waiterGetOwnTableList$','pack.waiter_table.waiterGetOwnTableList'),
    url(r'^waiterGetTableDetail$','pack.waiter_table.waiterGetTableDetail'),
    url(r'^setTableStatus$','pack.waiter_table.setTableStatus'),

    url(r'^submitOrder$','pack.waiter_order.submitOrder'),
    url(r'^addSkusWithOrder$','pack.waiter_order.addSkusWithOrder'),
    url(r'^waiterCancelOrderSku$','pack.waiter_order.waiterCancelOrderSku'),
    url(r'^waiterFinishOrder$','pack.waiter_order.waiterFinishOrder'),
    url(r'^waiterGetShopOrderListWithTable$','pack.waiter_order.waiterGetShopOrderListWithTable'),
    url(r'^waiterGetShopOrderDetailWithTable$','pack.waiter_order.waiterGetShopOrderDetailWithTable'),
    url(r'waiterGetShopDoingOrderList$','pack.waiter_order.waiterGetShopDoingOrderList'),
    url(r'^waiterGetShopOrderDetail$','pack.waiter_order.waiterGetShopOrderDetail'),

    url(r'^orderSeparateAddInfo$','pack.orderSeparate.orderSeparateAddInfo'),
    url(r'^orderSeparateGetInfo$','pack.orderSeparate.orderSeparateGetInfo'),
    url(r'^orderSeparateAlterInfo$','pack.orderSeparate.orderSeparateAlterInfo'),
    url(r'^alterOrderSeparateName$','pack.orderSeparate.alterOrderSeparateName'),
    url(r'^alterOrderSeparateHeadImage$','pack.orderSeparate.alterOrderSeparateHeadImage'),
    url(r'^orderSeparateFeedback$','pack.orderSeparate.orderSeparateFeedback'),
    url(r'^orderSeparateUpdateClientID$','pack.orderSeparate.orderSeparateUpdateClientID'),

    url(r'^orderSeparateGetCurrentOrderSkuList$','pack.orderSeparate_order.orderSeparateGetCurrentOrderSkuList'),
    url(r'^orderSeparateFinishOrderSkuList$','pack.orderSeparate_order.orderSeparateFinishOrderSkuList'),


    url(r'^beforeCookAddInfo$','pack.beforeCook.beforeCookAddInfo'),
    url(r'^beforeCookGetInfo$','pack.beforeCook.beforeCookGetInfo'),
    url(r'^beforeCookAlterInfo$','pack.beforeCook.beforeCookAlterInfo'),
    url(r'^alterBeforeCookName$','pack.beforeCook.alterBeforeCookName'),
    url(r'^alterBeforeCookHeadImage$','pack.beforeCook.alterBeforeCookHeadImage'),
    url(r'^beforeCookFeedback$','pack.beforeCook.beforeCookFeedback'),
    url(r'^beforeCookUpdateClientID$','pack.beforeCook.beforeCookUpdateClientID'),

    url(r'^beforeCookGetCurrentOrderSkuList$','pack.beforeCook_order.beforeCookGetCurrentOrderSkuList'),
    url(r'^beforeCookFinishOrderSkuList$','pack.beforeCook_order.beforeCookFinishOrderSkuList'),

    url(r'^cookAddInfo$','pack.cook.cookAddInfo'),
    url(r'^cookGetInfo$','pack.cook.cookGetInfo'),
    url(r'^cookAlterInfo$','pack.cook.cookAlterInfo'),
    url(r'^alterCookName$','pack.cook.alterCookName'),
    url(r'^alterCookHeadImage$','pack.cook.alterCookHeadImage'),
    url(r'^cookFeedback$','pack.cook.cookFeedback'),

    url(r'^cookGetOrderSkuList$','pack.cook_order.cookGetOrderSkuList'),

    url(r'^afterCookAddInfo$','pack.afterCook.afterCookAddInfo'),
    url(r'^afterCookGetInfo$','pack.afterCook.afterCookGetInfo'),
    url(r'^afterCookAlterInfo$','pack.afterCook.afterCookAlterInfo'),
    url(r'^alterAfterCookName$','pack.afterCook.alterAfterCookName'),
    url(r'^alterAfterCookHeadImage$','pack.afterCook.alterAfterCookHeadImage'),
    url(r'^afterCookFeedback$','pack.afterCook.afterCookFeedback'),
    url(r'^afterCookUpdateClientID$','pack.afterCook.afterCookUpdateClientID'),

    url(r'^afterCookGetCurrentOrderSkuList$','pack.afterCook_order.afterCookGetCurrentOrderSkuList'),
    url(r'^afterCookFinishOrderSkuList$','pack.afterCook_order.afterCookFinishOrderSkuList'),


    url(r'^serveAddInfo$','pack.serve.serveAddInfo'),
    url(r'^serveGetInfo$','pack.serve.serveGetInfo'),
    url(r'^serveAlterInfo$','pack.serve.serveAlterInfo'),
    url(r'^alterServeName$','pack.serve.alterServeName'),
    url(r'^alterServeHeadImage$','pack.serve.alterServeHeadImage'),
    url(r'^serveFeedback$','pack.serve.serveFeedback'),

    url(r'^serveGetCurrentOrderSkuList$','pack.serve_order.serveGetCurrentOrderSkuList'),
    url(r'^serveFinishOrderSkuList$','pack.serve_order.serveFinishOrderSkuList'),

    url(r'^testPush$','pack.orderSeparate_order.testPush'),

    url(r'^','pack.webViews.index'),
    url(r'^shopProtocol$','pack.webViews.shopProtocol'),
    url(r'^userProtocol$','pack.webViews.userProtocol'),
    ( r'^js/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.STATIC_URL+'js/'}
    ),

    ( r'^css/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.STATIC_URL+'css/' }
    ),

    ( r'^img/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.STATIC_URL+'img/' }
    ),
    ( r'^assets/(?P<path>.*)$', 'django.views.static.serve',
            { 'document_root': settings.STATIC_URL+'img/' }
    ),)
