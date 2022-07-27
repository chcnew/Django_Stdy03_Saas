#! /usr/bin/env python
# -*- coding:utf-8 -*-
# vim:fenc=utf-8

import os
import sys
import django

# 将项目目录saas加入到环境变量
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys路径添加，其包含的目录可以直接导入，无需附带路径
sys.path.append(base_dir)
# 加载配置文件，并启动一个虚拟的django服务
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
django.setup()
