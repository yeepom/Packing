#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#���ʺ�
accountSid= 'aaf98f894c5a7f75014c5e8fc41101bf';

#���ʺ�Token
accountToken= '7e1bcd25cc1c47ccb4c81cc4cc9ac37b';

#Ӧ��Id
appId='aaf98f894c7d3aca014c92b74b6c0b03';

#�����ַ����ʽ���£�����Ҫдhttp://
serverIP='app.cloopen.com';

#����˿� 
serverPort='8883';

#REST�汾��
softVersion='2013-12-26';

  # ������֤��
  # @param verifyCode ��֤�����ݣ�Ϊ���ֺ�Ӣ����ĸ�������ִ�Сд������4-8λ
  # @param playTimes ���Ŵ�����1��3��
  # @param to ���պ���
  # @param displayNum ��ʾ�����к���
  # @param respUrl ������֤��״̬֪ͨ�ص���ַ����ͨѶƽ̨�����Url��ַ���ͺ��н��֪ͨ

def voiceVerify(verifyCode,playTimes,to,displayNum,respUrl):
    #��ʼ��REST SDK
    rest = REST(serverIP,serverPort,softVersion)
    rest.setAccount(accountSid,accountToken)
    rest.setAppId(appId)
    
    result = rest.voiceVerify(verifyCode,playTimes,to,displayNum,respUrl)
    print result
    return result
'''    for k,v in result.iteritems():
        
        if k=='VoiceVerify' :
                for k,s in v.iteritems(): 
                    print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
   
'''
#voiceVerify('��֤������','���Ŵ���','���պ���','��ʾ�����к���','������֤��״̬֪ͨ�ص���ַ')