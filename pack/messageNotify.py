#encoding:gbk
import base64,urllib,urllib2,sys

reload(sys)
sys.setdefaultencoding('gbk')

#method = 1, ��ʼ���Ͷ������ѣ�method = 2���̼��¶����������ѣ�method = 3���û�ȡ���������ѡ�
def notify(telephone, method):
    if method == '1':
        print '1'
        content_msg = '����͡����Ķ����Ѿ�׼��������'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response

    elif method == '2':
        print '2'
        content_msg = '����͡������¶�������򿪿���̼Ұ�鿴�������ؿͻ��˲鿴��'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response
    elif method == '3':
        print '3'
        content_msg = '����͡����ж�����ȡ���ˣ���򿪿���̼Ұ�鿴��������ɲ���Ҫ���˷ѡ�'
        params = urllib.urlencode({'method':'sendSMS','username':774660874,'password':base64.encodestring('774660874'),'smstype':'1','mobile':telephone,'isLongSms':'0','content':content_msg})
        url_req = "http://114.215.136.186:9008/servlet/UserServiceAPI"
        sms_req = urllib2.Request(url = url_req, data = params)
        sms_response = urllib2.urlopen(sms_req)
        sms_response=sms_response.read()
        return sms_response



