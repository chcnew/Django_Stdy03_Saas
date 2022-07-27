# -*- coding:utf-8 -*-
import re


# 返回以什么开头以什么结尾的片段（包含开头结尾）
def piece(content):  # 获取字符片段
    # str_lsta = re.compile('(https://|http://)(.*?)(png|jpg|jpeg|gif|webp)').findall(content)
    str_lsta = re.compile('myqcloud.com/(.*?)(png|jpg|jpeg|gif|webp)').findall(content)
    str_lstb = ["".join(item) for item in str_lsta]

    return str_lstb
