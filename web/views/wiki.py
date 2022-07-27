# -*- coding:utf-8 -*-
import time
from django.http import JsonResponse
from django.shortcuts import reverse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from web import models
from web.myforms.wiki import WikiModelForm
from utils.tencent import cos
from utils.encrypt import uuid_md5
from utils import snippet


def manage_wiki(request, project_id):
    """wiki首页"""
    wiki_id = request.GET.get("wiki_id")
    # 为空或者不是十进制数,不满足条件不进入文档
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, "web/manage_wiki.html")
    else:
        wiki_row_obj = models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project).first()
        return render(request, "web/manage_wiki.html", {"wiki_row_obj": wiki_row_obj})


def wiki_add(request, project_id):
    """新建文档"""
    if request.method != "POST":
        form = WikiModelForm(request)
        form.instance.project_id = project_id
        return render(request, "web/wiki_add_edit.html", {"form": form})
    else:
        form = WikiModelForm(request, data=request.POST)
        if form.is_valid():
            # 填入没有project，保存当前项目信息到数据库
            form.instance.project_id = project_id

            # 考虑到要编辑文档，可能会选择id小于自身id的文档作为父文档
            # 需要处理是否选择了父文档判断,自身是否已作为父文档出发考虑
            if form.instance.parent:  # 如果用户选择父文档，则有
                form.instance.depth = form.instance.parent.depth + 1
            else:  # 如果用户没有选择父文档，则有
                form.instance.depth = 0
            form.save()
            wiki_row_obj = models.Wiki.objects.all().order_by("-id").first()
            # 脚本中附带参数反向解析地址
            url = reverse("manage_wiki", kwargs={"project_id": project_id})
            preview_url = "{}?wiki_id={}".format(url, wiki_row_obj.id)
            return redirect(preview_url)  # 跳转到当前文档预览
        else:
            return render(request, "web/wiki_add_edit.html", {"form": form})


def wiki_catalog(request, project_id):
    """文档目录"""
    queryset_wiki = models.Wiki.objects.filter(project_id=project_id).values("id", "title", "parent").order_by("depth", "id")
    return JsonResponse({"status": True, "data": list(queryset_wiki)})


def wiki_edit(request, project_id, wiki_id):
    """编辑文档"""
    wiki_row_obj = models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project).first()
    picture_before = snippet.piece(wiki_row_obj.content)  # 编辑前
    if request.method != "POST":
        form = WikiModelForm(request, instance=wiki_row_obj)
        return render(request, "web/wiki_add_edit.html", {"form": form})
    else:
        form = WikiModelForm(request, data=request.POST, instance=wiki_row_obj)
        if form.is_valid():
            # 考虑到要编辑文档，可能会选择id小于自身id的文档作为父文档
            # 需要处理是否选择了父文档判断,自身是否已作为父文档出发考虑
            if form.instance.parent:  # 如果用户选择父文档，则有
                form.instance.depth = form.instance.parent.depth + 1
            else:  # 如果用户没有选择父文档，则有
                form.instance.depth = 0

            # 编辑cos文件的处理
            picture_after = snippet.piece(form.instance.content)  # 编辑后
            if len(set(picture_before)) > len(set(picture_after)):
                del_picture = set(picture_before) - set(picture_after)
                for item in del_picture:
                    # print(item, "  ", request.tracer.project.bucket)
                    cos.cos_delete_object(request.tracer.project.bucket, item)

            form.save()
            # 脚本中附带参数反向解析地址
            url = reverse("manage_wiki", kwargs={"project_id": project_id})
            preview_url = "{0}?wiki_id={1}".format(url, wiki_id)
            return redirect(preview_url)  # 跳转到当前文档预览
        else:
            return render(request, "web/wiki_add_edit.html", {"form": form})


def wiki_delete(request, project_id, wiki_id):
    """删除文档"""
    time.sleep(1)

    if not wiki_id:
        return JsonResponse({"status": False})
    else:
        # 点击删除传回当前文档id

        queryset = models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project)

        # cos删除相关图片
        del_picture = snippet.piece(queryset.first().content)
        for item in del_picture:
            cos.cos_delete_object(request.tracer.project.bucket, item)
        # 删除数据行
        queryset.delete()
        return JsonResponse({"status": True})


@csrf_exempt
def wiki_upload(request, project_id):
    """图片上传"""
    image_obj = request.FILES.get("editormd-image-file")  # file_obj.name：文件名
    file_suffix = image_obj.name.split(".")[-1]
    after_name = "{}.{}".format(uuid_md5(request.tracer.user.phone), file_suffix)

    while True:  # 假设当前文件已经存在，则需要一直重新生成名称，基本不会执行，以防万一.
        if cos.cos_object_exists(request.tracer.project.bucket, after_name):
            after_name = "{}.{}".format(uuid_md5(request.tracer.user.phone), file_suffix)
        else:
            break

    # 执行文件上传，同时返回上传文件的url
    image_url = cos.wiki_upload(
        bucket=request.tracer.project.bucket,
        body=image_obj,
        key=after_name,
    )

    # 按格式将数据返回给Markdown的js回调函数
    result = {
        "success": 1,
        "url": image_url,
    }

    return JsonResponse(result)
