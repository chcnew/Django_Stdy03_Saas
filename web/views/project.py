# -*- coding:utf-8 -*-
import time
import datetime
from web.myforms.project import *
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.tencent import cos


@csrf_exempt
def project_list(request):
    # print(type(request.tracer.user), request.tracer.user)  # <class 'web.models.User'> chc
    # print(type(request.tracer.price_policy), request.tracer.price_policy)  # <class 'web.models.Price_Policy'> 免费版
    if request.method != "POST":
        # 项目展示
        project_dict = {"star": [], "my": [], "join": []}
        project_row_lst = models.Project.objects.filter(creator=request.tracer.user)
        for row in project_row_lst:
            if row.star:
                project_dict["star"].append(row)
            else:
                project_dict["my"].append(row)

        project_user_objs = models.ProjectUser.objects.filter(participant=request.tracer.user)
        for row in project_user_objs:
            if row.star:  # 只获取到非我创建，但我参与的，创建项目与参与者的没有设置初始化
                project_dict["star"].append(row.project)  # 获取关联的项目信息对象
            else:
                project_dict["join"].append(row.project)
        else:
            pass

        # 项目添加
        form = ProjectModelForm(request)
        return render(request, "web/project_list.html", {"form": form, "project_dict": project_dict})
    else:
        form = ProjectModelForm(request, data=request.POST)
        if form.is_valid():
            # 创建桶名，格式：用户手机号-创建时间-自定义后缀（依赖网速）
            bucket_user_phone = request.tracer.user.phone
            bucket_create_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")
            bucket = "{}-{}-{}".format(bucket_user_phone, bucket_create_time, "saas-1310871600")
            region = "ap-chengdu"

            while True:  # 假设当前桶已经存在，则需要一直重新生成名称，基本不会执行，以防万一.
                if cos.cos_bucket_exists(bucket):
                    bucket = "{}-{}-{}".format(bucket_user_phone, bucket_create_time, "saas-1310871600")
                else:
                    break

            cos.cos_create_bucket(bucket)
            # 新建项目需要视图函数初始化关联字段
            form.instance.bucket = bucket
            form.instance.region = region
            form.instance.creator = request.tracer.user
            instance = form.save()

            # 初始化当前项目默认问题类型
            issue_type_list = []
            for item in models.IssueType.INIT_ISSUE_TYPE:
                issue_type_list.append(models.IssueType(title=item, project=instance))
            models.IssueType.objects.bulk_create(issue_type_list)  # 批量添加数据行

            # 初始化当前项目文件模块根目录文件夹
            folders_list = []
            for item in models.FileLibrary.INIT_FOLDERS:
                folders_list.append(models.FileLibrary(project=instance, local_name=item, file_type=2, update_user=request.tracer.user))
            models.FileLibrary.objects.bulk_create(folders_list)  # 批量添加数据行

            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": form.errors})


def project_star(request, project_type, project_id, tf):
    if project_type == "my" and tf == "true":
        # my转为星标项目
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect("project_list")

    elif project_type == "join" and tf == "true":
        # join转为星标项目
        # 时刻注意ProjectUser表存入的是项目对象全部信息，project_id代表跨表id
        project_obj = models.ProjectUser.objects.filter(project_id=project_id, participant=request.tracer.user).update(star=True)
        return redirect("project_list")

        # my取消星标项目
    elif project_type == "my" and tf == "false":
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect("project_list")
        # join取消星标项目
    elif project_type == "join" and tf == "false":
        project_obj = models.ProjectUser.objects.filter(project_id=project_id, participant=request.tracer.user).update(star=False)
        return redirect("project_list")

    else:
        pass
