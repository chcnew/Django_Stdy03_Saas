# -*- coding:utf-8 -*-
import base
# 往数据库添加数据:链接数据库、操作、关闭链接
from web import models
from utils.encrypt import md5

# models.User.objects.create(username='chenshuo', password=md5('cs123321'), email='chengshuo@live.com', phone='13838383838')
row = models.Deal.objects.filter(id=1).first()
print(row.get_status_display())
