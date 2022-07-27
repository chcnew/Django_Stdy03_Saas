# -*- coding:utf-8 -*-
import base
from web import models

models.IssueType.objects.create(
    title="Bug",
    project=13,
)
models.Issue.objects.create(
    title="功能",
    project=13,
)
models.Issue.objects.create(
    title="任务",
    project=13,
)
print("\n操作完成！")
