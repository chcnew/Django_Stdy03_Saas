# -*- coding:utf-8 -*-
from web import models
from django import forms
from web.myforms.bootstrap import *
from web.myforms.widgets import ColorRadioSelect  # 继承源码RadioSelect类之后自定义颜色样式的类
from django.core.exceptions import ValidationError


class ProjectModelForm(BootStrapModelForm):
    """新建项目"""
    bootstrap_exclude_filed = ["color", "desc"]  # 不加bootstrap样式

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = models.Project
        fields = ["project_name", "color", "desc"]
        widgets = {
            "desc": forms.Textarea(attrs={"class": "form-control size-desc"}),
            # "color": forms.RadioSelect(),
            "color": ColorRadioSelect(attrs={"class": "color-radio"}),  # 自定义插件
        }

    def clean_project_name(self):
        """
            校验：
            1. 同一个用户创建的项目不能同名；
            2. 当前用户是否还有空间创建项目（价格策略）
        """
        txt_project_name = self.cleaned_data.get("project_name")
        # 验证自己创建的项目中，不能有同名项目
        # allow_count = self.request.tracer.price_policy.project_num
        allow_count = 100  # 测试允许创建最大100个项目
        count = models.Project.objects.filter(creator=self.request.tracer.user).count()
        # print(count, allow_count)
        if count >= allow_count:
            raise ValidationError("你的项目数量已达到上限！")

        exist = models.Project.objects.filter(project_name=txt_project_name, creator=self.request.tracer.user).exists()
        if exist:
            raise ValidationError("不被允许创建同名项目!")

        return txt_project_name


class DeleteProjectModelForm(BootStrapModelForm):
    """删除项目校验名称"""

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = models.Project
        fields = ["project_name"]

    def clean_project_name(self):
        txt_project_name = self.cleaned_data.get("project_name")
        delete_obj = models.Project.objects.filter(project_name=txt_project_name)

        if not delete_obj.exists():
            raise ValidationError("项目名称有误，没有找到该项目！")

        if delete_obj.first().creator != self.request.tracer.user:
            raise ValidationError("项目不属于你创建的！")

        delete_obj = models.Project.objects.filter(project_name=txt_project_name, creator=self.request.tracer.user)
        if not delete_obj:
            raise ValidationError("项目不存在，或已被删除!")

        return txt_project_name
