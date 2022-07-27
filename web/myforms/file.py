# -*- coding:utf-8 -*-
from web import models
from django import forms
from web.myforms.bootstrap import *
from django.core.exceptions import ValidationError
from utils.tencent import cos
from qcloud_cos.cos_exception import CosServiceError


class FileModelForm(BootStrapModelForm):
    """文件/文件夹"""

    def __init__(self, request, parent_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.parent_obj = parent_obj  # 当前url目录的对应的对象（以此作为父对象的查询）

    class Meta:
        model = models.FileLibrary
        fields = ["local_name"]

    def clean_local_name(self):
        txt_local_name = self.cleaned_data.get("local_name")
        queryset = models.FileLibrary.objects.filter(local_name=txt_local_name, file_type=2, project=self.request.tracer.project)
        # 判断当前项目的文件管理的文件目录下(父id相同)是否存在同名文件夹，当父对象为空，就去查根目录
        exist = queryset.filter(parent=self.parent_obj).exists()  # 查询同一个父目录的所有文件
        if exist:
            raise ValidationError("该目录下已存在同名文件！")
        else:
            pass
        return txt_local_name


class CheckFileModelForm(forms.ModelForm):
    """文件上传单个校验"""

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    ETag = forms.CharField(label="ETag")

    class Meta:
        model = models.FileLibrary
        fields = ["local_name", "cos_key", "parent", "file_size", "file_path"]

    def clean_file_path(self):
        txt_ETag = self.cleaned_data.get("file_path")
        return "https://{}".format(txt_ETag)

    def clean(self):  # 全部字段
        """校验每次post发送的ETag与cos查询是否相同"""
        txt_ETag = self.cleaned_data.get("ETag")
        txt_cos_key = self.cleaned_data.get("cos_key")
        txt_file_size = self.cleaned_data.get('file_size')

        try:
            # 后端查询的ETag与post的比对
            result_dict = cos.cos_head_object(bucket=self.request.tracer.project.bucket, key=txt_cos_key)
        except CosServiceError as e:
            self.add_error("cos_key", '数据库不允许存入未成功上传至Cos的文件数据！')
            return self.cleaned_data

        if txt_ETag != result_dict.get("ETag"):
            self.add_error("ETag", "文件存入ETag数据错误！")
            return self.cleaned_data

        elif int(result_dict.get('Content-Length')) != txt_file_size:
            self.add_error('size', '文件存入大小数据错误！')
            return self.cleaned_data

        else:
            return self.cleaned_data
