# -*- coding:utf-8 -*-
import hashlib
import uuid

from django.conf import settings


def md5(data_str):
    obj = hashlib.md5(settings.SECRET_KEY.encode("utf-8"))  # 自定义字符部分
    obj.update(data_str.encode("utf-8"))  # 连接编码
    return obj.hexdigest()  # 加密编码并返回


def uuid_md5(string):
    data = "{}-{}".format(uuid.uuid4(), string)
    return md5(data)
