# -*- coding:utf-8 -*-
import re
import random
from django import forms
from web import models
from django.conf import settings
from utils.encrypt import md5
from utils.tencent.sms import send_sms_single
from web.myforms.bootstrap import *
from django.db.models import Q
from django_redis import get_redis_connection
from django.core.exceptions import ValidationError


class GetSmsForm(forms.Form):
    """点击验证码--单独校验手机号码，单独提交场景"""
    tpl = forms.CharField(label="短信模板")
    phone = forms.CharField(label="手机号")

    def clean_phone(self):
        """校验手机号码钩子函数"""
        txt_tpl = self.cleaned_data.get("tpl")
        txt_phone = self.cleaned_data.get("phone")
        template_id = settings.TENCENT_TEMPLATE.get(txt_tpl)

        if not template_id:
            raise ValidationError("云短信模板不存在！")

        if len(txt_phone) != 11 or not re.findall(r'1[3-9]\d{9}', txt_phone):
            raise ValidationError("手机号码格式错误！")

        if txt_tpl == "register":  # 如果是注册，则执行
            exist = models.User.objects.filter(phone=txt_phone).exists()
            if exist:
                raise ValidationError("该号码已经注册！")

        if txt_tpl == "login":  # 如果是登录，则执行
            exist = models.User.objects.filter(phone=txt_phone).exists()
            if not exist:
                raise ValidationError("该号码不存在，请先注册！")

        code = str(random.randrange(100000, 999999))
        print(code)
        # sms = send_sms_single(txt_phone, template_id, [code, ])  # 字典类型，含错误提示信息。
        # if sms.get("result") != 0:
        #     raise ValidationError("发送短信失败，{}".format(sms.get("errmsg")))

        conn = get_redis_connection()
        # conn.set(txt_phone, code, ex=60)  # {号码:短信验证码} 存入redis缓存中，60秒后失效
        conn.set("15885464645", code, ex=120)  # {号码:短信验证码} 存入redis缓存中，60秒后失效
        return txt_phone


class UserRegisterModelForm(BootStrapModelForm):
    """用户注册"""
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True))

    smscode = forms.CharField(
        label="短信验证码",
        widget=forms.TextInput()
    )

    class Meta:
        model = models.User
        fields = ['username', 'password', 'confirm_password', 'email', 'phone', 'smscode']
        widgets = {"password": forms.PasswordInput(render_value=True)}

    # 钩子函数数据校验
    def clean_username(self):
        txt_username = self.cleaned_data.get("username")
        exist = models.User.objects.filter(username=txt_username).exists()
        if exist:
            raise ValidationError("该用户已存在！")
        else:
            return txt_username

    def clean_password(self):
        txt_password = self.cleaned_data.get("password")
        if len(txt_password) < 8:
            raise ValidationError("密码至少8个字符!")
        elif len(txt_password) > 64:
            raise ValidationError("密码至多64个字符!")
        else:
            return md5(txt_password)

    def clean_confirm_password(self):
        txt_password = self.cleaned_data.get("password")
        txt_confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if txt_password != txt_confirm_password:
            raise ValidationError("密码输入不一致！")
        else:
            return txt_confirm_password

    def clean_email(self):
        # 邮箱格式会自动校验，创建表的字段为EmailField
        txt_email = self.cleaned_data.get("email")
        exist = models.User.objects.filter(email=txt_email).exists()
        if exist:
            raise ValidationError("该邮箱已经注册！")
        else:
            return txt_email

    def clean_phone(self):
        txt_phone = self.cleaned_data.get("phone")
        if re.findall(r'1[3-9]\d{9}', txt_phone):
            exist = models.User.objects.filter(phone=txt_phone).exists()
            if exist:
                raise ValidationError("该号码已经注册！")
            else:
                return txt_phone
        else:
            raise ValidationError("手机号码格式错误！")

    def clean_smscode(self):
        txt_phone = self.cleaned_data.get("phone")
        txt_smscode = self.cleaned_data.get("smscode")
        conn = get_redis_connection()  # 十进制编码字符 123456，redis中为二进制编码
        byte_phone = conn.get(str(txt_phone))  # 3.0之后的redis库不支持空类型获取，需转为""
        if not byte_phone:
            raise ValidationError("请先获取有效的验证码！")
        else:
            if byte_phone.decode("utf-8") != txt_smscode:
                raise ValidationError("短信验证码错误！")
            else:
                return txt_smscode


class UserLoginForm(BootStrapForm):
    """用户登录"""

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    username = forms.CharField(
        label="用户名/邮箱/手机号",
        widget=forms.TextInput()
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True)
    )

    imgcode = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"style": "height: 30px;"})
    )

    def clean_password(self):
        txt_username = self.cleaned_data.get("username")
        txt_password = md5(self.cleaned_data.get("password"))
        # 原则上在使用关于数据库查询语句的时候，尽量简洁，节省开销，
        # 考虑到后边也需要查询，所以通过获取数据行，判断获取的数据行是否为空
        # 复杂条件查询Q语法
        exist = models.User.objects.filter(Q(username=txt_username) | Q(email=txt_username) | Q(phone=txt_username)).filter(password=txt_password).exists()
        if not exist:
            raise ValidationError("用户名或密码错误！")
        else:
            return txt_password

    def clean_imgcode(self):
        txt_username = self.cleaned_data.get("username")
        txt_password = self.cleaned_data.get("password")
        keycode = self.request.session.get("keycode")
        txt_imgcode = self.cleaned_data.get("imgcode")

        if not keycode:
            raise ValidationError("验证码已过期(60秒失效)！")

        if keycode.upper() != txt_imgcode.upper():
            raise ValidationError("验证码错误！")
        else:
            # 全部满足登录条件，存入session、cookie
            user_row_obj = models.User.objects.filter(Q(username=txt_username) | Q(email=txt_username) | Q(phone=txt_username)).filter(password=txt_password).first()
            if user_row_obj:
                self.request.session["userinfo"] = {"id": user_row_obj.id, "username": user_row_obj.username}
                self.request.session.set_expiry(60 * 60 * 24 * 7)
                return txt_imgcode


class SmsLoginForm(BootStrapForm):
    """ 手机号登录 """

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    phone = forms.CharField(
        label="手机号",
        widget=forms.TextInput()
    )

    smscode = forms.CharField(
        label="短信验证码",
        widget=forms.TextInput()
    )

    def clean_phone(self):
        txt_phone = self.cleaned_data.get("phone")
        if re.findall(r'1[3-9]\d{9}', txt_phone):
            exist = models.User.objects.filter(phone=txt_phone).exists()
            if not exist:
                raise ValidationError("该手机号码未注册！")
            else:
                return txt_phone
        else:
            raise ValidationError("手机号码格式错误！")

    def clean_smscode(self):
        txt_phone = self.cleaned_data.get("phone")
        txt_smscode = self.cleaned_data.get("smscode")
        conn = get_redis_connection()  # 十进制编码字符 123456
        str_smscode = conn.get(str(txt_phone))  # 二进制编码字符 b"123456"
        if not str_smscode:  # 判断redis中是否存在有效的验证码
            raise ValidationError("请先获取有效的验证码！")
        elif str_smscode.decode("utf-8") != txt_smscode:
            raise ValidationError("短信验证码错误！")
        else:
            user_row_obj = models.User.objects.filter(phone=txt_phone).first()
            if user_row_obj:
                self.request.session["userinfo"] = {"id": user_row_obj.id, "username": user_row_obj.username}
                self.request.session.set_expiry(60 * 60 * 24 * 7)
                return txt_smscode
