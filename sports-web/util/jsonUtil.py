# -*- coding: utf-8 -*-
__author__ = 'blankyin'

import simplejson
from web.utils import IterBetter, Storage


class JSONEncoder(simplejson.JSONEncoder):
    def getObjFields(self, Storage):
        """
        获取instance的字段与值
        """
        fields = Storage.keys()

        data = {}
        for attr in fields:
            data[attr] = getattr(Storage, attr)

        return data

    def default(self, obj):
        if isinstance(obj, IterBetter):
            result = []
            for item in obj:
                result.append(self.getObjFields(item))
            return result
        if hasattr(obj, 'isoformat'):
            return obj.isoformat(' ')   # 使用空格代替T
        return simplejson.JSONEncoder.default(self, obj)


def getJson(**args):
    """
    可以自定义Json规则
    """
    result = dict(args)
    return simplejson.dumps(result, cls=JSONEncoder)

