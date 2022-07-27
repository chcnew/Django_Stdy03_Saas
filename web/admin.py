# -*- coding:utf-8 -*-
from web import models
from django.apps import apps
from django.contrib import admin

admin.site.site_title = '系统后台'  # 设置标题
admin.site.site_header = '管理员登录'  # 设置标题

web_models = apps.get_app_config("web").get_models()
for model in web_models:
    admin.site.register(model)
