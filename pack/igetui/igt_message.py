__author__ = 'wei'

from pack.igetui.template.igt_base_template import *
class IGtMessage:
    def __init__(self):
        self.isOffline = False
        self.offlineExpireTime = 0
        self.data = BaseTemplate()
        self.pushNetWorkType = 0

class IGtSingleMessage(IGtMessage) :
    def __init__(self):
        IGtMessage.__init__(self)

class IGtListMessage(IGtMessage):
    def __init__(self):
        IGtMessage.__init__(self)

class IGtAppMessage(IGtMessage):
    def __init__(self):
        IGtMessage.__init__(self)
        self.appIdList = []
        self.phoneTypeList = []
        self.provinceList = []
        self.tagList = []
