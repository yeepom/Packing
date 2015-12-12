#encoding:gbk
import base64,urllib,urllib2,sys

reload(sys)
sys.setdefaultencoding('gbk')

#method = 1, 开始配送订单提醒；method = 2，商家新订单短信提醒；method = 3，用户取消订单提醒。
def notify(telephone, method):
    if method == '1':
        print '1'
        content_msg = '【快客】您的订单已经准备好啦！'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response

    elif method == '2':
        print '2'
        content_msg = '【快客】您有新订单，请打开快客商家版查看，或下载客户端查看。'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response
    elif method == '3':
        print '3'
        content_msg = '【快客】您有订单被取消了，请打开快客商家版查看，以免造成不必要的浪费。'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response



