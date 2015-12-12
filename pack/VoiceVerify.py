#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*-  

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= 'aaf98f894c5a7f75014c5e8fc41101bf';

#主帐号Token
accountToken= '7e1bcd25cc1c47ccb4c81cc4cc9ac37b';

#应用Id
appId='aaf98f894c7d3aca014c92b74b6c0b03';

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com';

#请求端口 
serverPort='8883';

#REST版本号
softVersion='2013-12-26';

  # 语音验证码
  # @param verifyCode 验证码内容，为数字和英文字母，不区分大小写，长度4-8位
  # @param playTimes 播放次数，1－3次
  # @param to 接收号码
  # @param displayNum 显示的主叫号码
  # @param respUrl 语音验证码状态通知回调地址，云通讯平台将向该Url地址发送呼叫结果通知

def voiceVerify(verifyCode,playTimes,to,displayNum,respUrl):
    #初始化REST SDK
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
#voiceVerify('验证码内容','播放次数','接收号码','显示的主叫号码','语音验证码状态通知回调地址')