# -*- coding:utf-8 -*-
import datetime
from web import models
from web.views import manage
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleWare(MiddlewareMixin):
    # 所有页面之前，可以设置url白名单
    def process_request(self, request):
        # 必须放在第一，函数调用前必须先初始化封装的值
        request.tracer = Tracer()  # 实例化对象

        # 未登录可以访问白名单页面
        if request.path_info in settings.URL_WHITE_LIST:
            return

        # 非白名单页面判断是否登录
        if not request.session.get("userinfo"):
            print("提示：访问非白名单url需要先登录！")
            return redirect('home_index')

        # 获取用户信息和最新交易记录，并存入方便调用
        user_row_obj = models.User.objects.filter(id=request.session["userinfo"].get("id")).first()  # 获取用户行对象
        request.tracer.user = user_row_obj
        deal_row_obj = models.Deal.objects.filter(trader=user_row_obj, status=2).order_by("-id").first()  # 最新的付费交易记录
        if deal_row_obj and deal_row_obj.end and (datetime.datetime.now() < deal_row_obj.end):
            # 当：付费版本&结束时间非空&结束时间>当前时间
            request.tracer.price_policy = deal_row_obj.price_policy

        # 否则：默认价格策略
        request.tracer.price_policy = models.PricePolicy.objects.filter(tos=1, level="个人免费").first()

    # 路由分发之后视图函数之前
    def process_view(self, request, manage_dashboard, args, kwargs):
        # 判断url是否是manage开头
        if not request.path_info.startswith("/web/manage/"):
            return

        project_id = kwargs.get("project_id")
        # 判断是否是我创建的项目
        project_row_obj = models.Project.objects.filter(id=project_id, creator=request.tracer.user).first()
        if project_row_obj:
            request.tracer.project = project_row_obj
            return

        # 判断是否是我参与的项目
        project_user_row_obj = models.ProjectUser.objects.filter(id=project_id, participant=request.tracer.user).first()
        if project_user_row_obj:
            request.tracer.project = project_user_row_obj.project
            return

        return redirect("project_list")
