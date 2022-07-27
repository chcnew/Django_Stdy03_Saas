# -*- coding:utf-8 -*-
from django import forms


class BootStrap(object):
    bootstrap_select_search_filed = []
    bootstrap_select_nosearch_filed = []
    bootstrap_exclude_filed = []

    # 给前端添加样式快速写法,与Meta类同级【工作必须使用】
    def __init__(self, *args, **kwargs):  # 有self，代表本函数内参数传递
        super().__init__(*args, **kwargs)  # 无self，使用父类方法，其实就是使用类Meta的对象
        # 循环找到所有插件，字典对象
        for name, field in self.fields.items():

            if name in self.bootstrap_exclude_filed:
                continue

            elif name in self.bootstrap_select_search_filed:
                field.widget.attrs = {
                    "class": "selectpicker form-control",
                    "data-live-search": "true",
                    "placeholder": "请输入" + str(field.label),
                }
                continue

            elif name in self.bootstrap_select_nosearch_filed:
                field.widget.attrs = {
                    "class": "selectpicker form-control",
                    "placeholder": "请输入" + str(field.label),
                }
                continue

            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": "请输入" + str(field.label),
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
