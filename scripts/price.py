# -*- coding:utf-8 -*-
import base
from web import models

if not models.PricePolicy.objects.filter(id=1).exists():
    models.PricePolicy.objects.create(
        tos=1,
        level="个人免费",
        price=0,
        project_num=5,
        member_num=5,
        project_space=20,
        up_filesize=5
    )
    print("\n操作完成！")
else:
    print("免费价格策略已存在！")

