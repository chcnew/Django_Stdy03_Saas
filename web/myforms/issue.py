# -*- coding:utf-8 -*-
from web import models
from django import forms
from web.myforms.bootstrap import *
from web.myforms.widgets import ColorSelect


class Issue(BootStrapModelForm):
    bootstrap_exclude_filed = ["follower"]
    bootstrap_select_search_filed = ["issue_type", "module", "receiver", "parent"]
    bootstrap_select_nosearch_filed = ["status", "priority", "mode"]

    class Meta:
        model = models.Issue
        exclude = ["project", "creator", "create_time", "update_time"]
        widgets = {
            "follower": forms.SelectMultiple(attrs={
                "data-live-search": "true",
                "data-actions-box": "true",
                "class": "selectpicker form-control",
            }),
            "priority": ColorSelect()
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        # 1.当前项目所有类型
        issue_type_objs_list = models.IssueType.objects.filter(project=self.request.tracer.project).values_list("id", "title")
        self.fields["issue_type"].choices = issue_type_objs_list
        # 2.当前项目所有模块
        module_objs_list = models.IssueModule.objects.filter(project=self.request.tracer.project).values_list("id", "title")
        self.fields["module"].choices = module_objs_list
        # 3.接收者和关注者(选择范围：当前项目创建者+当前项目参与者)
        init_user_list = [(request.tracer.project.creator.id, request.tracer.project.creator.username), ]
        participant_list = models.ProjectUser.objects.filter(project=request.tracer.project).values_list("participant_id", "participant__username")
        init_user_list.extend(participant_list)
        self.fields["receiver"].choices = init_user_list
        self.fields["follower"].choices = init_user_list
        # 4.父问题
        parent_list = models.Issue.objects.all().values_list("id", "title")
        self.fields["parent"].choices = parent_list
