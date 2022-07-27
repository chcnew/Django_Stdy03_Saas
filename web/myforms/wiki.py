# -*- coding:utf-8 -*-
from web import models
from django import forms
from web.myforms.bootstrap import *


class WikiModelForm(BootStrapModelForm):
    """wiki功能"""

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # select在前端显示选择（这里针对project只能选择自己创建或参与的项目）
        choice_lst = [("", "请选择")]
        wiki_lst = models.Wiki.objects.filter(project=request.tracer.project).values_list("id", "title")
        choice_lst.extend(wiki_lst)

        self.fields["parent"].choices = choice_lst

    class Meta:
        model = models.Wiki
        exclude = ["project", "depth", "picture"]
