# -*- coding:utf-8 -*-
# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 引擎选择 此处为mysql对应的引擎
        'NAME': 'saas',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'CONN_MAX_AGE': 7,  # 优化并发机制
        'PASSWORD': 'Cc158854@',  # 数据库密码
        'HOST': '192.168.127.140',  # ip地址
        'PORT': '3306',  # 端口号
    }
}

# 云短信业务配置
TENCENT_APPID = "xxx"  # 自己应用ID
TENCENT_APPKEY = "xxx"  # 自己应用Key
TENCENT_SMS_SIGN = "Python知识分享"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）

# 对象存储配置
COS_SECRET_ID = "xxx"
COS_SECRET_KEY = "xxx"

# redis配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.127.140:6399",  # 安装redis的主机的IP和端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "Cc158854@"  # redis密码
        }
    }
}
