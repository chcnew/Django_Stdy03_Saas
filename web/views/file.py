# -*- coding:utf-8 -*-
import json
from web import models
from django.http import JsonResponse
from django.shortcuts import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import F

from utils.tencent import cos
from django.views.decorators.csrf import csrf_exempt
from web.myforms.file import FileModelForm, CheckFileModelForm

import requests  # 文件下载分块处理方法
from django.utils.encoding import escape_uri_path


def manage_file(request, project_id):
    """文件/文件夹列表 & 新建文件夹"""
    parent_obj = None
    # 拼接url进入就获取参数.../？folder_id="XXX"
    folder_id = request.GET.get("folder_id", "")
    if folder_id and folder_id.isdecimal():
        # 获取当前url目录对应的数据库的文件夹对象信息(以此作为父对象)
        parent_obj = models.FileLibrary.objects.filter(id=int(folder_id), project=request.tracer.project, file_type=2).first()

    if request.method != "POST":

        # 文件导航处理,以当前目录为准，向上查找
        result_lst = []
        parent = parent_obj
        while parent:
            result_lst.insert(0, {"parent_id": parent.id, "parent_name": parent.local_name})
            parent = parent.parent

        # result_lst = [
        #     {"parent_id": "", "parent_name": "文件管理"},
        #     {"parent_id": "", "parent_name": "我的文档"},  # 列表首页: parent_id=null
        #     {"parent_id": "", "parent_name": "我的视频"},  # 上级目录: 我的文档
        # ]

        # 继续获取该文件夹下的文件及文件夹信息前端展示
        form = FileModelForm(request, parent_obj)
        objs = models.FileLibrary.objects.filter(project=request.tracer.project, parent=parent_obj).order_by("-file_type")
        context = {
            "form": form,
            "objs": objs,
            "result_lst": result_lst,
            "parent_obj": parent_obj,  # 用于传给上传文件时，数据库创建文件信息的父对象
        }
        return render(request, "web/manage_file.html", context)
    else:
        form = FileModelForm(request, parent_obj, data=request.POST)
        if form.is_valid():
            form.instance.file_type = 2
            form.instance.project = request.tracer.project
            form.instance.update_user = request.tracer.user
            # 需要考虑当前所在目录位置是否为根目录...
            form.instance.parent = parent_obj  # 创建的文件夹父对象就是当前所在url目录
            form.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": form.errors})


def file_edit(request, project_id):
    """编辑操作"""
    parent_obj = None
    fid = request.GET.get("fid", "")  # 文件或文件夹id
    fext = request.GET.get("fext", "")  # 文件或文件夹的后缀（文件夹为空）
    folder_id = request.GET.get("folder_id", "")  # 当前编辑文件的父id
    if folder_id and folder_id.isdecimal():
        # 获取当前url目录对应的数据库的文件夹对象信息(以此作为父对象)
        parent_obj = models.FileLibrary.objects.filter(id=int(folder_id), project=request.tracer.project, file_type=2).first()

    f_row_obj = models.FileLibrary.objects.filter(id=fid, project=request.tracer.project).first()
    form = FileModelForm(request, parent_obj, data=request.POST, instance=f_row_obj)
    if form.is_valid():
        # print(fext)
        if fext:  # 判断后缀是否为空
            form.instance.local_name = form.instance.local_name + "." + fext
        form.save()
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False, "errors": form.errors})


def file_edit_getdata(request, project_id):
    """编辑前获取原本数据展示"""
    fid = request.GET.get('fid')  # fid表示文件或文件夹数据行id
    f_row_obj = models.FileLibrary.objects.filter(id=fid, project=request.tracer.project).values().first()
    if f_row_obj:
        return JsonResponse({"status": True, "data": f_row_obj})
    else:
        return JsonResponse({"status": False, "error": "该文件或文件夹不存在,请刷新重试！"})


def file_delete(request, project_id):
    """删除文件或文件夹"""
    fid = request.GET.get('fid', "")  # fid表示文件或文件夹数据行id
    delete_obj = models.FileLibrary.objects.filter(id=fid, project=request.tracer.project).first()  # 一定要记得加项目限制，不然其他人随便传一个id就可以删除了
    if not delete_obj:
        return JsonResponse({"status": False, "error": "文件或文件夹不存在！"})

    # 实现删除文件
    if delete_obj.file_type == 1:
        # 1.cos删除
        cos.cos_delete_object(bucket=delete_obj.project.bucket, key=delete_obj.cos_key)
        # 2.数据库删除+当前项目归还数据空间
        if request.tracer.project.used_space < delete_obj.file_size:
            request.tracer.project.used_space = 0
            request.tracer.project.save()
        else:
            request.tracer.project.used_space = F("used_space") - delete_obj.file_size
            request.tracer.project.save()

        delete_obj.delete()
        return JsonResponse({"status": True})

    else:
        # 实现删除文件夹，删除所有以他为父目录的文件或文件夹，逐级删除, 一边循环元素，一边判断添加元素
        key_list = []
        total_size = 0
        folder_objs = [delete_obj, ]
        for folder in folder_objs:
            child_objs = models.FileLibrary.objects.filter(parent=folder, project=request.tracer.project).order_by("-file_type")
            for child in child_objs:
                if child.file_type == 2:
                    folder_objs.append(child)
                else:  # 文件
                    total_size += child.file_size  # 文件大小汇总
                    # cos删除文件装入列表
                    key_list.append({"Key": child.cos_key})

        # print(key_list) # [{},{}...]
        # 1.cos删除
        cos.cos_delete_objects(bucket=request.tracer.project.bucket, key_list=key_list)
        # 2.数据库删除+当前项目归还数据空间
        delete_obj.delete()
        if request.tracer.project.used_space < total_size:
            request.tracer.project.used_space = 0
            request.tracer.project.save()
        else:
            request.tracer.project.used_space = F("used_space") - total_size
            request.tracer.project.save()
        return JsonResponse({"status": True})


@csrf_exempt
def file_cos(request, project_id):
    """获取cos临时凭证"""
    check_str = request.POST.get("check_str")  # 获取post提交的字符串
    check_list = json.loads(check_str)  # 字符串转为列表
    # print(check_list) # 列表：[{'name': '头像x.png', 'size': 169216}]

    total_size = 0
    # 数据库创建上传的文件数据行
    for item in check_list:  # item {"name":"xxx","size":54552.1235}
        f_name = item.get("name")
        f_size = item.get("size")
        total_size += f_size
        # 与价格策略限制单文件比较
        # 上传的文件大小是字节（B）单位，与价格策略设置比较
        f_limit = request.tracer.price_policy.up_filesize * 1024 * 1024  # MB->字节
        # 字节比较
        if f_limit < f_size:
            return JsonResponse({'status': False, 'error': "单个文件上传限制{}MB，文件：{}；大小：{}MB；超出限制!".format(request.tracer.price_policy.up_filesize, f_name, round(f_size / 1024 / 1024))})

    # 判断当前已使用空间+增加的文件总空间是否大于项目允许最大空间
    used_space = request.tracer.project.used_space + total_size
    project_space = request.tracer.price_policy.project_space * 1024 * 1024 * 1024  # GB->字节

    if used_space > project_space:
        return JsonResponse({'status': False, 'error': "项目空间最大限制{}GB，上传的文件总大小超出限制!".format(request.tracer.price_policy.project_space)})
    else:  # 满足条件允许上传
        result_dict = cos.upload_credential(bucket=request.tracer.project.bucket, region=request.tracer.project.region)
        return JsonResponse({'status': True, 'get_data': result_dict})


@csrf_exempt
def file_post(request, project_id):
    """每次上传成功post一个创建一个数据到数据库"""
    # print(request.POST)  # 表单数据 queryDict:...
    form = CheckFileModelForm(request, data=request.POST)  # 校验model
    if not form.is_valid():
        return JsonResponse({"status": False, "errors": form.errors})
    else:
        # 校验通过：数据写入到数据库
        data_dict = form.cleaned_data
        data_dict.pop('ETag')
        data_dict.update({
            'file_type': 1,
            'project': request.tracer.project,
            'update_user': request.tracer.user
        })

        instance = models.FileLibrary.objects.create(**data_dict)  # instance为创建的数据行对象

        # request.tracer.project.used_space += data_dict["file_size"]  # 单线程修改字段值可用赋值方法
        request.tracer.project.used_space = F("used_space") + data_dict["file_size"]  # 多post请求，多线程并发资源竞争问题解决方法
        request.tracer.project.save()

        if not instance.parent:
            pid = None
        else:
            pid = instance.parent.id

        # 返回给前端显示当前添加的行数据
        show_data = {
            "fid": instance.id,
            "pid": pid,
            "local_name": instance.local_name,
            "file_size": instance.file_size,
            "update_user": instance.update_user.username,
            "update_time": instance.update_time.strftime("%Y年%#m月%d日 %H:%M"),
            # href请求地址
            "download_path": reverse("file_download", kwargs={"project_id": request.tracer.project.id, "fid": instance.id}),
        }
        return JsonResponse({"status": True, "show_data": show_data})

    # ModelForm保存到数据库
    # models.FileLibrary.objects.create(
    #     file_type=1,
    #     cos_key=request.POST.get("cos_key"),
    #     local_name=request.POST.get("local_name"),
    #     parent_id=request.POST.get("parent_id"),
    #     file_size=request.POST.get("file_size"),
    #     project=request.tracer.project,
    #     file_path="https://" + request.POST.get("file_path"),
    #     update_user=request.tracer.user,
    # )


def file_download(request, project_id, fid):
    """ 下载文件 """

    file_object = models.FileLibrary.objects.filter(id=fid, project=request.tracer.project).first()
    # 文件分块处理（适用于大文件）
    res = requests.get(file_object.file_path)  # 文件url
    data = res.iter_content()

    # 设置content_type=application/octet-stream 用于提示下载框
    response = HttpResponse(data, content_type="application/octet-stream")

    # 设置响应头：中文文件名转义
    response['Content-Disposition'] = "attachment; filename={};".format(escape_uri_path(file_object.local_name))
    return response
