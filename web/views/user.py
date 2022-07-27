# -*- coding:utf-8 -*-
import uuid
import datetime
from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from web.myforms.user import *
from utils.checkcode import check_code

from web import models
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_sms(request):
    """ 注册--云短信业务实现
        设置url参数发送云短信模板
        ?tpl=login —> 1359927
        ?tpl=register —> 1359933
        ?tpl=reset_password —> 1359916
    """
    # request对象作为参数传入钩子函数校验
    form = GetSmsForm(data=request.POST)
    if form.is_valid():
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False, "errors": form.errors})


def user_register(request):
    """用户注册"""
    if request.method != "POST":
        form = UserRegisterModelForm()
        return render(request, "web/user_register.html", {"form": form})
    else:
        exist = models.PricePolicy.objects.all()  # 判断是否添加了价格策略
        if not exist:
            return JsonResponse({"status": False, "price_policy_error": "数据库价格策略为空！"})

        form = UserRegisterModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            # 注册成功，需要将用户信息（行对象）存入交易记录用户列
            user_row_obj = form.instance  # 数据存入行对象且赋值
            # 创建交易记录(默认购买免费版)
            price_row_obj = models.PricePolicy.objects.filter(tos=1, level="个人免费").first()
            models.Deal.objects.create(
                status=2,
                order_num=str(uuid.uuid4()),
                trader=user_row_obj,
                price_policy=price_row_obj,
                payment=0,
                year_num=0,
                start=datetime.datetime.now(),
            )
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": form.errors})


def user_imgcode(request):
    """密码登录验证码"""
    img, code_str = check_code()
    request.session["keycode"] = code_str
    request.session.set_expiry(60)
    # 图片存至内存再取出
    stream = BytesIO()
    img.save(stream, 'png')
    value = stream.getvalue()
    return HttpResponse(stream.getvalue())


def user_login(request):
    """用户登录"""
    if request.method != "POST":
        form = UserLoginForm(request)
        return render(request, "web/user_login.html", {"form": form})
    else:
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": form.errors})


def sms_login(request):
    if request.method != "POST":
        form = SmsLoginForm(request)
        return render(request, "web/sms_login.html", {"form": form})
    else:
        form = SmsLoginForm(request, data=request.POST)
        if form.is_valid():
            return JsonResponse({"status": True})
        else:

            return JsonResponse({"status": False, "errors": form.errors})


def user_logout(request):
    request.session.flush()
    return redirect("home_index")


def user_setting(request):
    return render(request, "web/user_setting.html")
