  # **Django学习笔记_B(Saas)**

# **实现一个轻量级项目在线管理平台（saas）**

**错误积累：**
```python
1\ 3.0之后的redis不支持空类型获取数据，需要str(None)转为 ""
2\ 未解决问题：如何让request的username值作为ModelForm的input框的初始化的值？
```



# **1. 第一期项目开始-涉及知识点**

## **1. 1. 虚拟环境：创建多个共存的运行环境**
```python
环境1：django1.0
环境2：django2.0
... ...
```


## **1. 2. 配置local_settings.py本地配置**

用于重写settings.py相关配置;local_settings.py本地配置一般比如保密的信息或者其他，这个文件不用交给测试人员。

在当前目录取用当前目录的文件，直接用**“.”**符号引用即可！

**settings.py末尾写入**
```python
try:
    from .local_settings import *
except ImportError:
    pass
```

**local_settings.py写入**
```python
# 设置允许访问网站的ip
ALLOWED_HOSTS = ["*"]


# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 引擎选择 此处为mysql对应的引擎
        'NAME': 'gx_day16',  # 数据库名称
        'USER': 'root',  # 数据库用户名
        'CONN_MAX_AGE': 7,  # 优化并发机制
        'PASSWORD': 'Cc158854@',  # 数据库密码
        'HOST': '192.168.127.130',  # ip地址
        'PORT': '3306',  # 端口号
    }
}
# 语言和时区
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```

**配置setting.py同级目录的__init__.py文件**
```
# 导入pymysql
import pymysql
pymysql.install_as_MySQLdb()
```

**思考：关于****local_settings.py的理解****?**
```
-开发  
-测试     各自本地配置信息  实现各自目的配置
-运维
```







## **1. 3. 腾讯云平台的应用**

1. sms短信功能，申请服务；
2. cos对象存储：云盘存储数据，项目中上传/下载/查看功能。

## **1. 4. 关于使用redis**

```
mysql :
    本地pymysql模块    -->     mysql数据库  ——>  行为:    (硬盘文件操作)
                                                        create table ***
                                                        insert into ***








redis :
    本地redis模块    -->     redis数据库  ——>  行为:    (内存操作)
                                                       set name="***" 10s   内存中有键值对：name="***"
                                                       get name 获取name对应值，
                                                       10s 超时时间，时间一到，自动清除。
                                                       
                                                       
本地安装redis模块和数据库，也可以实现操作。
```



# **2. 项目分期简要规划**

- **一期：用户认证（登录+注册+短信认证+验证码 ==> djangoModelForm组件实现）**
- **二期：wiki、文件、问题管理**
- **三期：支付功能、项目部署（linux平台）**

## **2.1. 项目的环境搭建及相关应用**
```python
1\ 虚拟环境（项目环境）
2\ 项目框架：local_settings.py
3\ git实战应用
4\ python与腾讯云sms平台发送短信认证
```

## **2.2. 创建python虚拟环境**
anaconda搭建: Anaconda_conda、pip命令管理
virtualenv搭建：下面叙述linux中的搭建
安装python依赖、下载安装python10(源码安装) 
```
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make

wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
tar -xvf Python-3.10.4.tgz
cd Python-3.10.4
./configure --prefix=/usr/local/python3
make && make install 
```

```
# 添加用户级环境变量 profile.d--好维护，不要直接删除.sh文件即可。
cd /etc/profile.d/
vim python3.sh
# 写入内容保存
export PATH="$PATH:/usr/local/python3/bin"
# 重载环境变量文件
source ../profile
# 查看当前环境变量是否存在
echo $PATH


# 更改pypi源为清华镜像源
python3 -m pip install --upgrade pip 
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


# 文件位置：Writing to /root/.config/pip/pip.conf
```

## **2.3. 安装virtualenv**
```
# 更新全部python包
pip install pip-review
pip-review --local --interactive

pip3 install virtualenv
```

## **2.4. 创建虚拟环境**
假设目前系统中含有python2.7和python3.9(不加参数用系统默认版本)
```
virtualenv 环境名称
virtualenv 环境名称 --python=python2.7
virtualenv 环境名称 --python=python3.9
```

## **2.5. 激活/退出虚拟环境**
~ 目录下会有创建的虚拟环境文件
```
cd ~ 
source ~/环境名称/bin/activate
deactivate
```

## **2.6. 查看虚拟环境列表**
```
workon+空格+按两次Tab键
```

## **2.7. 删除虚拟环境操作**
```
rmvirtualenv 环境名称　
```



# **3. 企业项目开发注意**

**以上步骤再企业中做开发，是必须的步骤！以免发生不必要的麻烦！**

**企业中，项目给别一般用git的方式，在****git****中可以忽略local****_****settings.py**

## **3.1. 设置git忽略文件：.gitignore**
```
### Django ###
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
*.sqlite3

### Pycharm ###
.idea/
.DS_Store


*.py[cod]
*$py.class


### database migrations ###
*/migrations/*.py
!*/migrations/__init__.py
```

## **3.2. git项目上传及下载**
```
# 上传项目
git init
git add .
git commit -m "项目创建"
git remote add origin https://e.coding.net/stainlesssteel/saas/saas.git
git push origin master


# 下载项目录
git clone https://e.coding.net/stainlesssteel/saas/saas.git
```

## **3.3. git云端管理平台**
```
github/coding/gitee/gitlab
gitlab：可以实现自己搭建代码托管平台（安全问题才会涉及）
```



# **4. 腾讯云短信业务**

**学习文档：** **https://docs.qq.com/doc/DWExob3lvSEdyYVpr**

## **4.1. 设置setting.py （提示作用）**
```
# 云短信业务配置
TENCENT_APPID = 666666666  # 自己应用ID
TENCENT_APPKEY = "66666666666666666666666666666666"  # 自己应用Key
TENCENT_SMS_SIGN = "云短信签名内容"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
# 方便url对应模板
TENCENT_TEMPLATE = {
    "login": 1359927,
    "register": 1359933,
    "reset_password": 1359916,
}
```

## **4.2. 设置local_setting.py （****正式信息）**
```
# 云短信业务配置
TENCENT_APPID = 140065****  # 自己应用ID
TENCENT_APPKEY = "5181492b50eab6746563be51cd******"  # 自己应用Key
TENCENT_SMS_SIGN = "Python知识分享"  # 自己腾讯云创建签名时填写的签名内容（使用公众号的话这个值一般是公众号全称或简称）
```

## **4.3. 设置sms.py （正式信息）**
```
... ...
from django.conf import settings


appid = settings.TENCENT_APPID
appkey = settings.TENCENT_APPKEY
sms_sign = settings.TENCENT_SMS_SIGN
... ...
```

## **4.4. 视图函数views.py** 
```
def register_sms(request):
    """ 设置url参数发送云短信模板
        ?tpl=login —> 1359927
        ?tpl=register —> 1359933
        ?tpl=reset_password —> 1359916
    """
    tpl = request.GET.get("tpl")
    template_id = settings.TENCENT_TEMPLATE.get(tpl)
    print(template_id)
    if not template_id:
        return JsonResponse({"status": False, "errors": "云短信模板不存在！"})
    else:
        code = random.randrange(100000, 999999)
        res = send_sms_single('1588546', template_id, [code, ])
        if res.get("result") == 0:
            request.session["userinfo"] = {"smscode": code}
            request.session.set_expiry(60)
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": res.get("errmsg")})
```

## **4.5. 前端代码**
```
<a class="btn btn-sm btn-success btn-block subbtn" href="/register/sms/?tpl=login">获取验证码</a>
```



# **5. 注册功能（细说短信验证码）**

## **5.1. 短信验证码实现思路**

- 注册页面呈现获取验证码按钮 —> get请求，附带参数 tpl=register 到路由。
- 输入手机号后点击获取，发送post提交 —> Ajax实现
- 验证码时效设置（60s）—> Redis缓存实现

![img](https://docimg3.docs.qq.com/image/SVRVMshDBQUJP_KyvTgU2A.png?w=925&h=560)     



# **6. 安装redis（linux）**

**Redis安装文档：****https://docs.qq.com/doc/DWG9oSnVxQ2JtQ0Nh**



# **7. Django依赖模块连接redis**

上述可以实现在django中操作redis。

但是，这种形式有点非主流，因为在django中一般不这么干，而是用另一种更加简便的的方式。

## **第一步：安装django-redis模块（内部依赖redis模块）**
```
pip3 install django-redis
```

## **第二步：在django项目的settings.py中添加相关配置**
```
... ...


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.28:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }
}


... ...
```

## **第三步：在django的视图中操作redis**
```
from django.shortcuts import HttpResponse
from django_redis import get_redis_connection
def index(request):
    # 去连接池中获取一个连接
    conn = get_redis_connection()
    conn.set('nickname', "诸葛亮", ex=10)
    value = conn.get('nickname')
    print(value)
    return HttpResponse("OK")
```

这样就可以实现在django中通过redis进行存取值，在后续的项目开发中可以用他来完成短信验证码过期的功能。



# **8. 内容回顾**

## **8.1. 基于virtualenv使用虚拟环境**
```
● virtualenv (每个项目创建独立虚拟环境)
● requirements.txt ( pip freeze > requirements.txt )
● local_settings.py
● gitignore
```

## **8.2. 腾讯云短信/阿里云短信（阅读文档，文档不清晰: 谷歌、必应、搜狗)**

- - **API，提供URL,你去访问这些URL并根据提示传参数。【所有第三方工具都有】**
```
requests.get("http : / / www.xxx.com// adsf/asdf/" , json={ ......})
```
- - **SDK，模块;下载安装模块，基于模块完成功能, 直接导入调用。**
```
# sms.py
def sms(var1, var2, ...):
    ... ...
```

## **8.3. Redis的使用方法(缓存处理)**
```
第一步：A主机（服务端) - 安装配置redis服务（/usr/local/redis/src/  redis-server）
第二步：A主机（客户端）- 客户端连接测试（/usr/local/soft/redis/bin/  redis-cli）
第三步：B主机（客户端）- python的redis模块连接（使用ip+密码）
```

**使用python的redis模块连接方法**(不要直接连接（直接跳过），**先创建连接池，再进行连接**)
```
import redis


# 创建redis连接池（默认连接池最大连接数 2**31=2147483648）
pool = redis.ConnectionPool(
    host='10.211.55.28', 
    port=6379, 
    password='foobared', 
    encoding='utf-8', 
    max_connections=1000
    )


# 去连接池中获取一个连接
conn = redis.Redis(connection_pool=pool)


# 设置键值：15131255089="9999" 且超时时间为10秒（值写入到redis时会自动转字符串）
conn.set('name', "诸葛亮", ex=10)


# 根据键获取值：如果存在获取值（获取到的是字节类型）；不存在则返回None
value = conn.get('name')


print(value)
```

**使用django-redis模块连接(支持多台主机连接：读写分离场景适用)**
```
... ...


CACHES = {
    "read": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.28:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }
    
    "write": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.211.55.29:6379", # 安装redis的主机的 IP 和 端口
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "foobared" # redis密码
        }
    }


}


... ...
```



# **9. 多app模板处理**

**当我们把setting.py的模板路径改为** **'DIRS': [], 模板寻找方式即为从外到内，根据app注册顺序从上至下查找templates目录下的文件，创建多个app的时候，我们需要在每个app路径下再创建一个目录与app同名，存放该app的所有模板文件，以此来区分各个app模板文件。**

![img](https://docimg7.docs.qq.com/image/xWYhGJTfJVpXC0OqlNfH4Q.png?w=1206&h=512)        

## **9.1. 多app路由设置**

**路由可以设置别名，当不同app设置相同路由别名时，需要增加namespace="app名称"，不然在反向解析时识别不出路由地址。**
```
# 第一个app informal


from django.urls import path
from informal.views import account


urlpatterns = [
    path('user/login/', account.user_login, name=login),
    path('user/register/', account.user_register),
]


# 第二个app web
from django.urls import path
from web.views import user


urlpatterns = [
    path('user/login/', user.user_login，name=login),
    path('user/register/', user.user_register),
    path('user/imgcode/', user.user_imgcode),
    path('register/sms/', user.register_sms),
]


# 底层路由
from django.contrib import admin
from django.urls import path, include
from web.views import user


urlpatterns = [
    path('admin/', admin.site.urls),
    path('informal/', include('informal.urls'), namespace='informal'),
    path('web/', include('web.urls'), namespace='web'),
]
```

## **9.2. 反向解析**
```
 <html>
<head>
    <title>反向解析</title>
</head>
<body>
普通链接：<a href="/login/">普通login</a>
<hr>
反向解析：<a href="{% url 'informal:login' %}">反向解析login</a>
</body>
</html>
```



# **10. 页面母板引用框架(**font-awesome为字体和图标框架**)**

```
{% load static %}
... ...
<link rel="stylesheet" href="{% static 'plugins/bootstrap/css/bootstrap.css' %}">
<link rel="stylesheet" href="{% static 'plugins/font-awesome/css/font-awesome.css' %}">
... ...
<!-- 如果使用插件，必须引入jQuery -->
<script type="text/javascript" src="{% static 'plugins/jquery/jquery-3.6.0.min.js' %}"></script>
<!-- 包括所有的bootstrap的js插件或者可以根据需要调用js插件调用 -->
<script type="text/javascript" src="{% static 'plugins/bootstrap/js/bootstrap.min.js' %}"></script>
... ...
```



# **11. 获取短信验证码**

**实现过程：**
```
1\ 按钮绑定点击事件
2\ 获取手机号
3\ 发送ajax
4\ 手机号校验
    ● 不能为空
    ● 格式正确
    ● 没有注册过
5\ 验证通过
    ● 发送短信
    ● 将短信保存到redis中(60s)
```

![img](https://docimg5.docs.qq.com/image/XWBdQD2gdYS9egqakAhUkw.png?w=1278&h=870)        

**思路：**

- **js：同时获取电话和url参数tpl=register，jquery中以id获取input值的方法：**$("#id").val()**

```
@csrf_exempt
def register_sms(request):
    """ 设置url参数发送云短信模板
        ?tpl=login —> 1359927
        ?tpl=register —> 1359933
        ?tpl=reset_password —> 1359916
    """
    # request对象作为参数传入钩子函数校验
    form = Register_Sms(request, data=request.POST)
    if form.is_valid():
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False, "errors": form.errors})
```

**视图函数中(views/user.py)：**

**新知识：request作为对象传入钩子函数（需要先对类初始化接收参数）进行校验**
```python
@csrf_exempt
def register_sms(request):
    """ 设置url参数发送云短信模板
        ?tpl=login —> 1359927
        ?tpl=register —> 1359933
        ?tpl=reset_password —> 1359916
    """
    # request对象作为参数传入钩子函数校验
    form = Register_Sms(request, data=request.POST)
    if form.is_valid():
        return JsonResponse({"status": True})
    else:
        return JsonResponse({"status": False, "errors": form.errors})
```

**form组件脚本中（forms/user.py）：** 

**新知识点：使用到了视图函数和钩子方法之间的交互，对类的__init__方法增加参数，同时继承父类forms.Form，这样就可以把对云短信模板是否存在判断，返回错误也集成到了form.errors中。**
```python
class Register_Sms(forms.Form):
    """点击验证码校验电话号码"""


    # 与视图函数交互写法,初始化接收参数
    def __init__(self, request, *args, **kwargs):
        super(Register_Sms, self).__init__(*args, **kwargs)
        self.request = request


    phone = forms.CharField(
        label="电话",
    )


    def clean_tpl(self):
        tpl = self.cleaned_data.get("phone")
        print(tpl)
        return tpl


    def clean_phone(self):
        """校验电话号码钩子函数"""
        tpl = self.request.POST.get("tpl")
        phone = self.cleaned_data.get("phone")
        template_id = settings.TENCENT_TEMPLATE.get(tpl)


        if not template_id:
            raise ValidationError("云短信模板不存在！")


        if not re.findall(r'1[3-9]\d{9}', phone):
            raise ValidationError("手机号格式错误！")


        exist = models.User.objects.filter(phone=txt_phone).exists()
        if exist:
            raise ValidationError("该号码已经注册！")


        code = random.randrange(100000, 999999)
        sms = send_sms_single(phone, template_id, [code, ])  # 字典类型，含错误提示信息。
        if sms.get("result") != 0:
            raise ValidationError("发送短信失败，{}".format(sms.get("errmsg")))


        return phone
```



# **12. js实现按钮不可点击属性和验证码显示倒计时**

## **12.1. 根据id添加按钮不可点击属性（.prop方法实现）**
```javascript
$("#getcode").prop("disabled",true);
$("#getcode").prop("disabled"false);
```

## **12.2. js定时器**
```javascript
var obj = setInterval(function () {
    console.log("1秒显示一次")
}, 1000)
```

## **12.3. 验证码倒计时显示**
```javascript
/* 验证码倒计时显示 */
function btn2Event() {
    $("#getcode").prop("disabled", true)
    var time = 60
    var remind = setInterval(function () {
        time = time - 1;
        $("#getcode").val(time + "秒重新获取");
        if(time < 1){
            $('#getcode').val("点击获取验证码").prop("disabled", false);
            clearInterval(remind)
        }
    }, 1000)
}
```

 **对于刷新之后按钮立即显示复原的问题，其实在云短信业务里面可以设置返回错误结果（收费版本可以是实现对于频率的提示，打包至字典的键为errmsg的值，包含在信息提示里面），会反馈到号码的错误提示；**

**经验总结：**

**1. 在写Form或者ModelForm初始化函数的时候，继承类的时候一定要记得初始化函数的样式（可以传参数）,有冒号  def** **__init__(self, request, \*args, \**kwargs):**

**而继承父类初始化方法的时候，样式 （没有冒号，没有多的参数，只有父类的参数）**

**super().__init__(\*args, \**kwargs)**   

**2. ****Ajax请求不会改变当前前端显示情况****，除非有返回值，经过js处理才会改变！**

**对部分字段进行校验，比如：**

![img](https://docimg8.docs.qq.com/image/W5W8RB84I-XISKQ0XWmHvQ.png?w=1280&h=523.2813559322034)        

# **13. 短信登录功能**
**开发思路：**
```
1\ 页面展示
2\ 点击发送短信
3\ 点击登录 
```
**由于之前做注册页面使用过短信验证，我们可以考虑直接使用注册页面模板实现前端，后端直接使用短信验证的函数即可，在里边做一个条件，可以是注册（tpl=register），登录（tpl=login)或者密码重置（reset_password）发过来的请求，判断是哪一个，并作出相应的反馈。**

**forms/user.py  实质上这个模板并不在前端注册页面显示出Input框，因为前端注册页面使用的是注册的模型。但是根据前端id=id_+字段 的属性，可以显示出错误提示。**
```python
class Get_Sms(forms.Form):
    """点击验证码--单独校验手机号码，单独提交场景"""
    tpl = forms.CharField(label="短信模板")
    phone = forms.CharField(label="手机号码")


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


        code = random.randrange(100000, 999999)
        sms = send_sms_single(txt_phone, template_id, [code, ])  # 字典类型，含错误提示信息。
        if sms.get("result") != 0:
            raise ValidationError("发送短信失败，{}".format(sms.get("errmsg")))


        conn = get_redis_connection()
        conn.set(txt_phone, code, ex=60)  # {号码:短信验证码} 存入redis缓存中，60秒后失效
        return txt_phone
```



# **14. 用户名+密码登录**
实现登陆界面+数据校验



## **14.1. 图片验证码(实现点击更换)**
```html
... ...


<div class="form-group">
    <div class="row row row-no-gutters">
        <div class="col-md-6 col-sm-6 col-xs-6">
            {{ form.imgcode }}
            <span class="error-msg"></span>
        </div>
        <div class="col-md-6 col-sm-6 col-xs-6  text-right">
            <img class="verification imgcode" src="{% url 'user_imgcode' %}" alt="验证码图片" onclick="this.setAttribute('src','{% url 'user_imgcode' %}?nocache='+Math.random());"/>
        </div> <!--验证码-->
    </div>
</div>



... ...
```

## **14.2. 视图函数**
```python
from io import BytesIO




def user_imgcode(request):
    """登录验证码"""
    img, code_str = check_code()
    request.session["keycode"] = code_str
    request.session.set_expiry(60)
    # 图片存至内存再取出
    stream = BytesIO()
    img.save(stream, 'png')
    value = stream.getvalue()
    return HttpResponse(stream.getvalue())
```



## **14.3. Cookie和Session回顾**

![img](https://docimg3.docs.qq.com/image/N9Ks_u6ar9tE1zW8bPKK_Q.png?w=1121&h=698)        

**1. 登录成功用户id和username存入session**
```python
# 全部满足登录条件，存入session、cookie
row_obj = models.User.objects.filter(Q(username=txt_username) | Q(email=txt_username) | Q(phone=txt_username)).filter(password=txt_password).first()
if row_obj:
    self.request.session["userinfo"] = {"id": row_obj.id, "username": row_obj.username}
    self.request.session.set_expiry(60 * 60 * 24 * 7)
```





**2. 导航设置登录前和登录后的区别**
```html
<ul class="nav navbar-nav navbar-right">
    {% if not request.session.userinfo.username %}
        <li><a href="{% url 'sms_login' %}">登 录</a></li>
        <li><a href="{% url 'user_register' %}">注 册</a></li>
    {% else %}
        <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{ request.session.userinfo.username }} <span class="caret"></span></a>
            <ul class="dropdown-menu">
                <li><a href="#">账号设置</a></li>
                <li><a href="{% url 'user_logout' %}">注销登录</a></li>
            </ul>
        </li>
    {% endif %}
</ul>hh
```





**也可以使用中间键，request创建键值对接收用户信息，一旦登录，一直存在。**

**创建 middleware/auth.py**
```python
from web import models
from django.utils.deprecation import MiddlewareMixin




class AuthMiddleware(MiddlewareMixin):
	def process_request(self,request):
    	# 如果用户已登录、则reauest中创建键值对 request = {... "tracer":{...} ...}
    	user_id = request.session.get('user_id')
    	row_obj = models.User.objects.filter(id=user_id).first()
    	request.tracer = row_obj
```



**注册 middleware / auth.py /** AuthMiddleware    **在settings.py文件中添加**
```python
INSTALLED_APPS = [
    ... ...
    'web.middleware.auth.AuthMiddleware'
    ... ...
]
```



# **15. 第一期项目结束（登录功能完成！）**

- **项目代码回顾**

- **思维导图，回顾技术点**

![img](https://docimg6.docs.qq.com/image/YYHy-9WyOUQ69Me9d21Y_g.png?w=1280&h=477.7570093457944)        



# **16. 第二期项目开始-离线脚本**

## **16.1. 工具类—运行环境base.py）**
```python
#! /usr/bin/env python
# -*- coding:utf-8 -*-
# vim:fenc=utf-8


import os
import sys
import django




# ------------------------------ 环境 -------------------------------------


    # 将项目目录saas加入到环境变量
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys路径添加，其包含的目录可以直接导入，无需附带路径
    sys.path.append(base_dir)
    # 加载配置文件，并启动一个虚拟的django服务
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "saas.settings")
    django.setup()


# ------------------------------ 脚本 ----------------------------------------


# Write your script... ...
```







## **16.2. 离线脚本运行-如插入数据 (script/init_user.py)**
```python
# -*- coding:utf-8 -*-
# ------------------------------ 环境 -------------------------------------
import base
# ------------------------------ 脚本 ----------------------------------------
# 往数据库添加数据:链接数据库、操作、关闭链接
from web import models
from utils.encrypt import md5


models.User.objects.create(username='chenshuo', password=md5('cs123321'), email='chengshuo@live.com', phone='13838383838')
```




# **17. 探讨业务**

## **17.1. 提知识点：创建对象存储COS存储数据**

基于腾讯对象存储的cos存储数据（文件、图片等）



## **17.2. 用户信息表(web_User)**

| **用户ID** | **用户名**   | **密码**                         | **邮箱**           | **手机号**  | **业务类型** |
| ---------- | ------------ | -------------------------------- | ------------------ | ----------- | ------------ |
| **id**     | **username** | **password**                     | **email**          | **phone**   | **tof**      |
| 1          | chc          | 04fe07473679594b9568d2c798b8d4a8 | chc@qq.com         | 14712312312 | 1            |
| 2          | chenshuo     | 79babd1b0a739d680b23aeb183cfae03 | chengshuo@live.com | 13838383838 | 1            |
| 3          | zgl          | 79babd1b0a739d680b23aeb183cfae03 | zgl@qq.com         | 17612824799 | 1            |



## **17.3. 价格策略(web_Price) ，以业务类型区分（免费 收费 其它）**

| **业务ID** | **业务类型** | **业务级别**      | **价格/年** | **项目创建数量上限** | **项目参与成员上限** | **项目空间上限(G)** | **单个文件上传大小限制(M)** | **创建时间**    |
| ---------- | ------------ | ----------------- | ----------- | -------------------- | -------------------- | ------------------- | --------------------------- | --------------- |
| **id**     | **tof**      | **level(字符型)** | **price**   | **project_num**      | **member_num**       | **project_space**   | **up_filesize**             | **create_time** |
| 1          | **1-免费**   | 个人免费          | 0           | 5                    | 5                    | 20                  | 5                           |                 |
| 2          | **2-收费**   | VIP               | 199         | 20                   | 100                  | 50                  | 500                         |                 |
| 3          | **2-收费**   | SVIP              | 299         | 50                   | 200                  | 100                 | 1024                        |                 |
| *          | **3-其他**   | *                 | *           | *                    | *                    | *                   | *                           |                 |

**注意：新用户默认有个人免费版的配置**



## **17.4. 交易记录表(web_Deal)**

| **交易记录ID** | **交易状态** | **订单号**    | **用户信息 ->** **用户行对象** | **价格 -> 业务ID** | **实际支付** | **购买数量（年）** | **业务开始时间** | **业务结束时间** |
| -------------- | ------------ | ------------- | ------------------------------ | ------------------ | ------------ | ------------------ | ---------------- | ---------------- |
| **id**         | **status**   | **order_num** | **user_info**                  | **price**          | **payment**  | **year_num**       | **start**        | **end**          |
| 1              | 已支付       | UY43          | 2                              | 1                  | 0            | 无限制             | 2022-4-10        | 无限制           |
| 2              | 待支付       | UY44          | 1                              | 3                  | 299          | 1                  | 2022-4-10        | 2023-4-10        |

实现可以考虑在登录后，数据存放至request.session中，或者使用中间件，登录后，request.tracer = row_obj方式。



## **17.5. 项目信息表【项目-用户关系1V1 】 (web_Project)**

| **项目ID** | **项目名称** | **显示颜色** | **项目描述** | **星标**    | **参与人数**   | **创建者 -> 用户ID** | **项目已使用空间** | **创建时间**    |
| ---------- | ------------ | ------------ | ------------ | ----------- | -------------- | -------------------- | ------------------ | --------------- |
| **id**     | **name**     | **color**    | **desc**     | **collect** | **member_num** | **creator**          | **used_space**     | **create_time** |
| 1          | CRM          | bule         | ***          | true        | 2              | 2                    | 10M                |                 |
| 2          | SAAS         | green        | ***          | false       | 3              | 1                    | 200M               |                 |





## **17.6. 项目参与表【项目-用户关系nVn】(web_Participant)**

| **参与表ID** | **项目名称 -> 项目ID** | **参与用户 -> 用户ID** | **星标**    | **邀请者（不做）** | **角色（不做）** |
| ------------ | ---------------------- | ---------------------- | ----------- | ------------------ | ---------------- |
| **id**       | **name**               | **user**               | **collect** |                    |                  |
| 1            | 1                      | 1                      | true        |                    |                  |
| 2            | 1                      | 2                      | false       |                    |                  |



# **18. 根据设计创建表结构**

## **18.1. 创建表结构**

![img](https://docimg4.docs.qq.com/image/_2okhPPqzkOVH4bzRXn9Sg.png?w=1280&h=617.7827547592385)        关联同一张表的时候，在**反向关联**时，就会识别不了，所以报错;

**反向关联，比如**
```python
row_obj = models.User.object.filter(id=1)
row_obj.Participant_set.all()
```



**此时，加上一个别名：****related_name="XXX"**
```python
user = models.ForeignKey(verbose_name="用户名", to="User", on_delete=models.CASCADE, related_name="A")
inviter = models.ForeignKey(verbose_name="邀请者", to="User", on_delete=models.CASCADE, related_name="B")
```





**反向关联改为：**
```python
row_obj = models.User.object.filter(id=1)
row_obj.A.all()
```



## **18.2. 离线脚本创建价格策略（免费版即可）**

| **业务ID** | **分类** | **标题**   | **价格/年** | **最多创建项目个数** | **项目成员上限** | **项目空间** | **单个文件上传大小限制** | **创建时间**    |
| ---------- | -------- | ---------- | ----------- | -------------------- | ---------------- | ------------ | ------------------------ | --------------- |
| **id**     | **type** | **title**  | **price**   | **number**           | **member**       | **space**    | **limit**                | **create_date** |
| 1          | 免费     | 个人免费版 | 0           | 5                    | 5                | 20M          | 5M                       |                 |


也可以使用后台管理：

指导文档：https://www.cnblogs.com/rainny/p/13853915.html

我的实现：
```python
# -*- coding:utf-8 -*-
from web import models
from django.apps import apps
from django.contrib import admin


admin.site.site_title = '系统后台'  # 设置标题
admin.site.site_header = '管理员登录'  # 设置标题


web_models = apps.get_app_config("web").get_models()
for model in web_models:
    admin.site.register(model)
```




# **19. 用户注册成功后初始化交易记录（赠送免费版）**

- 新建用户；
- 新建交易记录(交易记录里面的用户为用户数据行信息，价格策略为价格策略数据行信息)。

```python
def user_register(request):
    """用户注册"""
    if request.method != "POST":
        form = User_Register()
        return render(request, "web/user_register.html", {"form": form})
    else:
        form = User_Register(data=request.POST)
        if form.is_valid():
            # 注册成功，需要将用户信息（行对象）存入交易记录用户列
            # 将数据存入数据库且同时返回当前行对象赋值
            user_row_obj = form.save()


            # 创建交易记录
            # price_row_obj = models.Price.objects.filter(tos=1).first()
            # models.Deal.objects.create(
            #     status=2,
            #     order_num=str(uuid.uuid4()),
            #     user=user_obj,
            #     price=price,
            #     payment=0,
            #     year_num=0,
            #     start=datetime.datetime.now(),
            # )


            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, "errors": form.errors})
```



# **20. 页面的中间件处理**

- **定义中间件类继承，settings.py注册，url白名单作为列表变量写到setting.py中，导入到中间件引用，**

**middelware/auth.py**

```python
# -*- coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin




class AuthMiddleWare(MiddlewareMixin):


    def process_request(self, request):
        # 未登录可以访问白名单页面
        if request.path_info in settings.URL_WHITE_LIST:
            return


        elif not request.session.get("userinfo"):
            print("访问非白名单url需要先登录！")
            return redirect('home_index')
        else:
            return
```



# **21. 新建项目**

- 项目样式处理；

样式可自己重写css，更改bootstrap相关样式

- 中间件权限处理

将白名单url设置到setting.py, 在中间件直接导入引用

- 注意数据表的项目创建者与用户关联，所以在数据提交保存数据库时，需要先对没有设置默认数据且是关联其他表的数据先进行初始化（form.instance.字段名 = XXX）

![img](https://docimg7.docs.qq.com/image/b7vQOMA6bG667JllqZQKXQ.png?w=1280&h=477.7337110481587)        

选择颜色：关于模板语言Radio设置option纵向改为横向+自定义样式

## **21.1 查看f源码：CTRL+鼠标左键**

![img](https://docimg3.docs.qq.com/image/2MKmJzjBdCPe2ELVl2oIhw.png?w=1280&h=603.4782608695652)        

![img](https://docimg8.docs.qq.com/image/pSNVSH-bSuNB9teSedDqIA.png?w=1280&h=697.7479492915735)        

![img](https://docimg1.docs.qq.com/image/PVLfn0M6p6f0o_ZPQ5AJhg.png?w=1280&h=587.2069464544139)        

知道了引用文件为同级目录下的templates里边的文件，可以复制到自己的app模板目录下，先继承RadioSelect类，再引用自己复制的文件路径：
```python
from django.forms.widgets import RadioSelect


class ColorRadioSelect(RadioSelect):
    # template_name = 'django/forms/widgets/radio.html'   # 默认
    # option_template_name = 'django/forms/widgets/radio_option.html'  # 默认
    template_name = 'web/widgets/color_radio/radio.html'
    option_template_name = 'web/widgets/color_radio/radio_option.html'
```





![img](https://docimg6.docs.qq.com/image/de8ZCpYn37qD9HF3oy-VtA.png?w=1280&h=543.8173747622068)        

导入就可以引用了~~，然后自己更改模板内容就可以了（难点在于需要懂模板语言~~）

## **21.2. Django RadioSelect默认垂直样式**
```
{% with id=widget.attrs.id %}
    <ul{% if id %} id="{{ id }}"{% endif %}{% if widget.attrs.class %} class="{{ widget.attrs.class }}"{% endif %}>{% for group, options, index in widget.optgroups %}{% if group %}
        <li>{{ group }}
        <ul{% if id %} id="{{ id }}_{{ index }}"{% endif %}>{% endif %}{% for option in options %}
        <li>{% include option.template_name with widget=option %}</li>{% endfor %}{% if group %}
        </ul></li>{% endif %}{% endfor %}
    </ul>{% endwith %}
```
![img](https://docimg9.docs.qq.com/image/tQD4IPDKGQklWdrrkzDZgg.png?w=1061&h=619) 

## **21.3. Django RadioSelect改为横向样式**	
```
{% with id=widget.attrs.id %}
    <div{% if id %} id="{{ id }}"{% endif %}{% if widget.attrs.class %} class="{{ widget.attrs.class }}"{% endif %}>
        {% for group, options, index in widget.optgroups %}
            {% for option in options %}
                <label {% if option.attrs.id %} for="{{ option.attrs.id }}"{% endif %} >
                    {% include option.template_name with widget=option %}
                </label>
            {% endfor %}
        {% endfor %}
    </div>
{% endwith %}
```
![img](https://docimg4.docs.qq.com/image/tRLMVH9hyG_afNdXMNpBTA.png?w=1001&h=424)



# **23. 展示项目**
```tex
1\ 从数据库获取两部分数据；
    我创建的所有项目，已星标，未星标
    我参与的所有项目，已星标，未星标
2\ 抓取已星标：
    我创建 和 参与的 星标项目
3\ 创建字典： 
    # 项目展示
    project_dict = {"star": [], "my": [], "join": []}
```

- 星标项目\我的项目\我的参与
```python
if request.method != "POST":
    # 项目展示
    project_dict = {"star": [], "my": [], "join": []}


    project_row_lst = models.Project.objects.filter(creator=request.tracer.user)
    for row_x in project_row_lst:
        if row_x.star:
            project_dict["star"].append(row_x)
        else:
            project_dict["my"].append(row_x)


    project_user_row_lst = models.ProjectUser.objects.filter(participant=request.tracer.user)
    for row_y in project_user_row_lst:
        if row_y.project not in project_row_lst:  # 只获取非我创建，但我参与的
            if row_y.star:
                project_dict["star"].append(row_y.project)  # 获取关联的项目信息对象
            else:
                project_dict["join"].append(row_y.project)
        else:
            pass
```
![img](https://docimg1.docs.qq.com/image/QF9khYYqw0ce62Gz7Ar8JQ.png?w=1247&h=898)        

CSS设置图标移入显示
```html
# 初始显示
.panel-body .project_item > .info a .on-star {
    color: #d5d5d5;
}
# 鼠标移入
.panel-body .project_item > .info a .on-star:hover {
    color: #f0ad4e;
}
```



# **23.1 inclusion_tag的使用（多个页面都需要显示的，用于同样方式从后端传数据场景）**

inclusion_tag在使用的时候可以帮我们减少很多前端和后端重复的代码

逻辑图：

![img](https://docimg1.docs.qq.com/image/Zo1-KCTBK1Duei9UzDZVGQ.png?w=800&h=452)        

 	inclusion_tag的作用是主页面以一定的语法给一个参数，调用某个函数，这个函数可以通过主页面给的参数做一些逻辑处理得到一些数据，将数据渲染到一个小html模块，然后将渲染后的小html模块返回给主页面渲染在调用的位置。

在使用自定义inclusion_tag的时候，我们需要在应用下面新建templatetags文件包，里面必须含有__init__.py文件，另外新建一个任意名称的py文件，里面的固定写法如图。

- 第一步：在app目录下创建templatetags包(包名只能是templatetags，不能改)
- 第三步：在包内，新建py文件（如：project_tags.py）
- 第四步：在模板文件下创建模板文件web/inclusion/all_project_list.html
- 清楚流程：

1. 前端引用：
```html
... ...
{% load project_tage %}
... ...
{% all_project_list %}   <!-- 指向project_tags.py函数名 -->
... ...
```



函数里面：写入想传递的数据，字典形式；
```python
# -*- coding:utf-8 -*-
# inclusion_tag ,传一个html模板文件
from django import template


register = template.Library()




@register.inclusion_tag('web/inclusion/all_project_list.html')
def all_project_list():  # 前端调用先load该py文件，再引用函数。
    # 返回必须是字典
    return {'name': '碎掉'}
```





1. 函数运行之后运行装饰器函数（执行模板渲染）

文件：web/inclusion/all_project_list.html



```
<div>碎吊的男人：{{ name }}</div>
```
![img](https://docimg5.docs.qq.com/image/nsXqRXWienRqVKjACHCo-w.png?w=1280&h=429.5238095238095)        



CSS a标签的5种状态
```
 a:link{color:#fff}  未访问时的状态（鼠标点击前显示的状态）
 a:hover{color:#fff}  鼠标悬停时的状态
 a:visited{color:#fff}  已访问过的状态（鼠标点击后的状态）
 a:active{color:#fff}  鼠标点击时的状态
 a:focus{color:#fff}  点击后鼠标移开保持鼠标点击时的状态[获得焦点]（只有在<a href="#"></a>时标签中有效）
```





# **24. 项目管理**

## **24.1. 路由规划**
```
manage/项目id/dashboard 概览
manage/项目id/issues 问题
manage/项目id/statistics 统计
manage/项目id/file 文件
manage/项目id/wiki 超文本编辑器系统
manage/项目id/setting 项目设置
```



## **24.2. 路由APP内再次分发及中间件****process_view函数**
```
path('manage/<int:project_id>/', include([
    path('dashboard/', manage.manage_dashboard, name='manage_dashboard'),
    path('issues/', manage.manage_issues, name='manage_issues'),
    path('statistics/', manage.manage_statistics, name='manage_statistics'),
    path('file/', manage.manage_file, name='manage_file'),
    path('wiki/', manage.manage_wiki, name='manage_wiki'),
    path('setting/', manage.manage_setting, name='manage_setting')
], namespace=None), None)
```



点击项目后，进入显示与项目相关的菜单 思路：
```tex
1\ 进入之前：http://127.0.0.1:8000/web/manage/1/dashboard/#
从请求url看出，需要确定你请求的项目是你的（要么是创建者，要么是参与者）；另一个要求就是以manage开头的url就是点击了项目进入后的效果。
2\ 
```



- 中间件 def process_view(): ... ...



```
用户请求 ——> 中间件process_request() ——> 匹配分发的路由id ——>process_view() ——> 视图函数...


执行流程：
首先执行 process_request 函数，然后在执行视图函数之前执行 process_view 函数，然后执行视图函数，最后执行 process_response 函数
```





**由此，要在request中获取信息，必须等到路由分发之后（ process_view() ）。**



```
# 路由分发之后视图函数之前
def process_view(self, request, manage_dashboard, args, kwargs):
    # 判断url是否是manage开头
    if not request.path_info.startswith("/web/manage/"):
        return


    project_id = kwargs.get("project_id")
    # 判断是否是我创建的项目
    project_row_obj = models.Project.objects.filter(id=project_id, creator=request.tracer.user).first()
    if project_row_obj:
        request.tracer.project = project_row_obj
        return


    # 判断是否是我参与的项目
    project_user_row_obj = models.ProjectUser.objects.filter(id=project_id, participant=request.tracer.user).first()
    if project_user_row_obj:
        request.tracer.project = project_user_row_obj.project
        return


    return redirect("project_list")
```



**注意：使用自定义类封装到request时，一定要记得在第一行就初始化，若写在其他函数之后，假设恰好该函数条件成立，直接往下走，则跳过了自定义封装类的初始化，后边就取不了值！**
![img](https://docimg5.docs.qq.com/image/ClF6k5MLn-7Jd3eZtx7Paw.png?w=1280&h=455.43391188250996)        



# **25. 进入项目，显示关于项目菜单**

## **25.1. 实现点击菜单进入后，一直为选中状态（就是按url在当前项目下，操作都基于当前url：/web/manage/100/dashboard/）：**
```
1\ 使用中间件存入的项目对象判断，是否可以进入项目；
2\ 进入项目后，显示出相关菜单（inclusion_tage实现）；
```
![img](https://docimg9.docs.qq.com/image/mdx_1IumohdYU4WIp-MdhQ.png?w=1280&h=258.9595375722543)        



**使用到了.py文件中先定义好反向解析****：reverse模块实现,传参数kwargs记得为字典类型！**
```python
data_lst = [
    {"title": "概览", "url": reverse("manage_dashboard", kwargs={"project_id": request.tracer.project.id})},
    {"title": "问题", "url": reverse("manage_issues", kwargs={"project_id": request.tracer.project.id})},
    {"title": "统计", "url": reverse("manage_statistics", kwargs={"project_id": request.tracer.project.id})},
    {"title": "文件", "url": reverse("manage_file", kwargs={"project_id": request.tracer.project.id})},
    {"title": "wiki", "url": reverse("manage_wiki", kwargs={"project_id": request.tracer.project.id})},
    {"title": "设置", "url": reverse("manage_setting", kwargs={"project_id": request.tracer.project.id})},
]
```



**使用到inclusion_tage就可以了！**



# **26. wiki页面功能**

## **26.1. wiki表结构设计**

| **id** | **title** | **project** | **content** | **parent** |
| ------ | --------- | ----------- | ----------- | ---------- |
|        | 标题      | 关联项目    | 内容        | 父ID       |

## **26.2. wiki首页展示（manage_wiki）**

![img](https://docimg9.docs.qq.com/image/kiu3dn6BFTQ9jwNNB5RGgw.png?w=1280&h=278)        

**实现思路：**面板+css+项目颜色的request里面获取

- **注意点：3+9布局、框线接壤处理：**margin-left: -1px; /*移动1像素，使得框线重合*/
```
/* wiki */
.title-list {
    border-right: 1px solid #dddddd;
    min-height: 800px;
}


.content {
    border-left: 1px solid #dddddd;
    margin-left: -1px; /*移动1像素，使得框线重合*/
    min-height: 800px;
    text-align: center;
    margin-top: 120px;


}


/*新建文章输入框样式*/
/*.container > form {*/
/*    margin-top: 10px;*/
/*}*/


.container > form .form-group #id_content {
    height: 240px;
    resize: vertical;
}
```



## **26.3. wiki添加文章（wiki_add）**
**modelform那一套之后，****需解决存在bug：当前项目也可以选择到其他项目的文章标题**
![img](https://docimg6.docs.qq.com/image/zX92CV31yEtcMv1f_yDhlw.png?w=1280&h=592.1680049413218)        
**由图可****知，parent字段子关联属于，choices=((),())方式显示；在modelform针对字段.choices方法时，可以重写显示的值：**
```python
class WikiModelForm(BootStrapModelForm):
    """wiki功能"""


    class Meta:
        model = models.Wiki
        exclude = ["project"]


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义字段在前端显示选择（这里针对project只能选择自己创建或参与的项目）
        self.fields["parent"].choices = [(1, "A"), (2, "B")]
```



**所以针对当前目录下，只能展示当前目录的相关文档，代码（设置默认为请选择）：**
```
class WikiModelForm(BootStrapModelForm):
    """wiki功能"""


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定义字段在前端显示选择（这里针对project只能选择自己创建或参与的项目）
        choice_lst = [(0, "请选择")]
        wiki_lst = models.Wiki.objects.filter(project=request.tracer.project).values_list("id", "title")
        choice_lst.extend(wiki_lst)


        self.fields["parent"].choices = choice_lst


    class Meta:
        model = models.Wiki
        exclude = ["project"]
```



## **26.4. 实现多级目录展示（同样也适用于多级评论的场景）**

- **实现思路：后端+前端ajax+id选择器**
```tex
1\ 前端：打开页面之后，发送ajax请求，获取当前项目在wiki数据库的信息，只取三列即可;
2\ 后端：使用查询 .values("","")拿到当前项目的querySet类型的数据:[{},{}]
例如拿到：[
    {'id':1, title:'王元', parent_id:None}, 
    {'id':2, title:'尹立生', parent_id:None}, 
    {'id':3, title:'王天然', parent_id:None}, 
    {'id':4, title:'杨力', parent_id:3}, 
    {'id':5, title:'张浩', parent_id:1}, 
]
返回到前端，
3\ 前端回调函数
success: function(res){
    $.each(res.data, function(index, item){
        if(item.parent_id){
        
        }else{
            
        }
    })
}


大概表达：
<ul>
	<li id="l">王元
		<ul>
			<li id='5'>张浩</li>
		</ul>
	</li>


	<li id="2">尹立生</li>
	<li id="3">王天然
		<ul>
			<li id='4'>杨力</li>
		</ul>
	</li>
</ul>
```



## **26.5. 多级目录存在的问题：**

**1. 假设修改修改当前文档父文档，父文档出现在其后边，则会显示不出来，因为创建目录默认获取数据按id顺序拿到的。**

**实现思路：**

**文档信息表增加一个字段 深度：depth 记录被作为父文档的次数，每次被选作为父目录就加1存入数据库；**

![img](https://docimg10.docs.qq.com/image/n0jcIwT6WbH_RKZV7b2SOQ.png?w=479&h=287)        

**2. 获取文档数据先按照depth排序，再按照id排序；**

**实现点击目录进入文章展示，****http://127.0.0.1:8000/web/manage/3/wiki/** **+ 设置参数：?wiki_id=文章id**
```python
JS:
...
//定义全局变量为wiki首页url /web/manage/3/wiki/  后边直接传入文档id
var MANAGE_WIKI_URL = "{% url 'manage_wiki' project_id=request.tracer.project.id %}"
...
var href = MANAGE_WIKI_URL + "?wiki_id=" + item.id
var li = $("<li>").attr("id", "id_" + item.id).append($("<a>").attr("href", href).text(item.title)).append($("<ul>"));


视图函数：GET请求，get方法获取参数
def manage_wiki(request, project_id):
    if request.GET.get("wiki_id"):
        print("文章详细")
    else:
        print("wiki首页")
    return render(request, "web/manage_wiki.html")
```



## **26.6. wiki编辑文章**

和添加没大的区别，基本都是，除了添加的时候，手动添加当前项目对象到数据库，其他没分别。

注意就是，编辑完成，跳转到当前编辑文章预览地址：
```python
# 脚本中附带参数反向解析地址
url = reverse("manage_wiki", kwargs={"project_id": project_id})
# 构造字符串地址：http://127.0.0.1:8000/web/manage/3/wiki/?wiki_id=23
preview_url = "{0}?wiki_id={1}".format(url, wiki_id)  
return redirect(preview_url)  # 跳转到当前文档预览
```



## **26.7. wiki删除文章**

只要将当前项目id及文章id传进函数，进行删除即可。考虑一个账号可以多个人同时登录的话，可能在删除文章的时候，
已经被删除，这个可以做个提示，或者做个判断直接略过，不然有可能会报错！
```python
def wiki_delete(request, project_id, wiki_id):
    if not wiki_id:
        return JsonResponse({"status": False})
    else:
        # 点击删除传回当前文档id
        models.Wiki.objects.filter(id=wiki_id, project=request.tracer.project).delete()
        return JsonResponse({"status": True})
```



#  **28. Markdown编辑器**

- 富文本编辑器：ckeditor
- markdown编辑器：meditor
- 项目中应用Markdown编辑器：

添加和编辑的页面中textarea输入框，转为markdown编辑器，

Markdown下载地址：
```tex
https://www.mdeditor.com/
https://github.com/pandao/editor.md
https://pandao.github.io/editor.md/examples/index.html
https://pandao.github.io/editor.md/examples/index.html
```



**Markdown及Cos使用详细：** https://docs.qq.com/doc/DWENoak1uTEpIQ3JJ
![img](https://docimg7.docs.qq.com/image/RNB3u7-g5A1pRRgFMz0UGw.png?w=1280&h=373.9476439790576)        

从用法中，我们在项目中如何应用Markdown编辑器已说明，这里继续说明创建桶的应用：

我们可以很方便的实现创建桶，所以，可以思考，将每个项目下边的文件都放在一个桶，这样就需要对创建项目时，增加一个标识，这就扩展数据库增加一列；

- 创建项目时创建桶

pycharm对函数，类等自动生成注解格式：设置+"""+enter键
![img](https://docimg8.docs.qq.com/image/0PN8p0sst6v6-egoMR1qJQ.png?w=1280&h=693.3333333333334)        

**解决数据提交延迟问题：**

**CSS样式：**
```css
/*提交等待*/
.submit_loading {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left:0;
    background-color: #000;
    text-align: center;
    opacity: 0.2;
 }
.loading_show {
    margin-top: 40%;
 }


.loading_context {
   margin-top:1%;
   color: #fff;
   font-size:11pt;
 }
```



**HTML设置等待提示(放于与当前最上层标签同级)：**
```html
<div id="loading" class="submit_loading" style="display: none">
    <div class="loading_show">
        <img src="{% static 'img/loading-sun.gif' %}" alt="">
        <p class="loading_context">请稍候...</p>
    </div>
</div>
```



**JS:**
```javascript
//表单提交提示
function Mask() {
    $('#loading').css({'display': 'block'});
}


function UnMask() {
    $('#loading').css({'display': 'none'});
}


function btnSaveEvent() {
    $("#btn_save").click(function () {
        Mask();
        $.ajax({
            url: "{% url 'project_list' %}",
            type: 'post',
            data: $("#add_form").serialize(),
            dataType: 'JSON',
            success: function (res) {
                UnMask()
            },
            error: function (res) {
                UnMask();
            },
        });
    })
}
```



# **29. 第二期项目结束- Markdown上传图片到对象存储**

## **问题需求分析及思路流程**

```tex
1\ 点击mrkdown按钮，显示出本地上传按钮；
2\ 点击本地上传，选择图片，post请求发送（csrf免验证）；
3\ 指定视图函数接收到文件对象：file_obj = request.FILE,
4\ 调用对象存储SDK文件上传（cos的python版本SDK内部自动会将文件对象处理为文件存储到云盘）；
   命名问题：上传同名文件会被替换，设置一个不重复的随机文件名再存储；
   文件为空：Markdown返回错误信息(内部方法:message)；
   存储成功：返回文件url地址，并且填入Markdown地址栏；
```



## **1-显示出本地上传按钮：****imageUpload****:** **true****,**  **//显示本地上传按钮**
```javascript
var UPLOAD_WIKI_URL = "{% url 'wiki_upload' project_id=request.tracer.project.id %}";


//Markdown初始化
function ininEditorMd() {
    editormd("editor", {
        placeholder: "请输入文档内容...",
        height: 560, //指定高度
        path: "{% static 'plugins/editor-md/lib/' %}",  //必须指定依赖文件位置（切记最后/结尾）
        imageUpload: true,  //显示本地上传按钮
        imageFormats: ["png", "jpg", "jpeg", "gif", "webp"],  //可以上传的文件类型
        imageUploadURL: UPLOAD_WIKI_URL,  //上传url，post请求
    })
}
```



## **2-调用定义好的使用SDK上传对象的视图函数**

**自定义函数传参、同时返回文件url：**
```python
def wiki_upload(bucket, body, key, region='ap-chengdu'):  # 文件对象上传
    secret_id = settings.COS_SECRET_ID  
    secret_key = settings.COS_SECRET_KEY
    region = region
    token = None
    scheme = 'https'


    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
    client = CosS3Client(config)




    # 上传对象方法，自动转为文件存入
    image_url = client.upload_file_from_buffer(
        Bucket=bucket,
        Body=body,  
        Key=key,
    )


    # 上传之后返回一个url--格式：https://dsa-1310871600.cos.ap-nanjing.myqcloud.com/%E5%A4%B4%E5%83%8Fx.png
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket, region, key)
```



**视图函数调用自定义函数，并传入参数：**
```
@csrf_exempt
def wiki_upload(request, project_id):
    image_obj = request.FILES.get("editormd-image-file")  # file_obj.name：文件名
    file_suffix = image_obj.name.split(".")[-1]
    after_name = "{}.{}".format(uuid_md5(request.tracer.user.phone), file_suffix)


    # 执行文件上传，同时返回上传文件的url
    image_url = cos.wiki_upload(
        bucket=request.tracer.project.bucket,
        body=image_obj,
        key=after_name,
    )


    # 按格式将数据返回给Markdown的js回调函数
    result = {
        "success": 1,
        "message": "上传成功！",
        "url": image_url,
    }


    return JsonResponse(result)
```



## **3-实现每次编辑，假设先上传，之后删除图片链接同步cos删除功能**

实现思路：
```python
1\ 进入编辑，记录初始的页面链接中的图片文件名（正则表达式处理），存为列表；
2\ 上传后修改后，再次正则获取文件名存为列表，
3\ 两个列表转为集合，求集合元素个数，假设前者大于后者，则用前者-后者得到差集，这就说明删除了图片；
4\ 循环取cos删除对象即可。
```



```python
# 编辑cos文件的处理
picture_after = snippet.piece(form.instance.content)  # 编辑后
if len(set(picture_before)) > len(set(picture_after)):
    del_picture = set(picture_before) - set(picture_after)
    for item in del_picture:
        # print(item, "  ", request.tracer.project.bucket)
        cos.wiki_delete_object(request.tracer.project.bucket, item)DJ
```



#  **30. 第三期项目开始-文件管理功能**
```tex
1\ 模态对话框 & ajax & 后台modelForm校验 目录切换︰展示当前文件夹&文件
2\ 删除文件夹：嵌套的子文件&子文件夹全部删除js上传文件到cos (wiki用python上cos上传文件)进度条的操作
3\ 删除文件
4\ - 我们数据库中删除
5\ - cos中这个文件也需要删除
6\ 下载文件
```



## **30.1. 设计思路梳理**

**JS前端上传文件到cos流程**

![img](https://docimg6.docs.qq.com/image/enmX8PLJ9GlUbHvwfE-U1Q.png?w=1145&h=469)        

## **30.2. 设计表结构**

| **id** | **项目id**  | **文件夹或文件名称** | **区分文件夹和文件—类型** | **文件存入cos名称** | **cos文件url** | **大小**      | **父目录（自关联）** | **最后使用者** | **最后使用时间** |
| ------ | ----------- | -------------------- | ------------------------- | ------------------- | -------------- | ------------- | -------------------- | -------------- | ---------------- |
|        | **project** | **local_name**       | **file_type**             | **cos_key**         | **file_path**  | **file_size** | **自关联**           | **last_user**  | **last_time**    |
| 1      | 项目对象    | asc.png              | 1                         | dfgdhhj.png         |                | 10M           | null                 | 用户对象       |                  |
|        |             |                      |                           |                     |                |               |                      |                |                  |



```python
class FileLibrary(models.Model):
    """wiki表结构设计"""


    class Meta:
        verbose_name = '文件仓库'  # 设置admin页面右边标题显示
        verbose_name_plural = '文件仓库'  # 设置admin页面左边导航显示


        # 设置后台显示信息


    def __str__(self):
        return str(self.local_name)


    project = models.ForeignKey(verbose_name="项目信息", to="Project", on_delete=models.CASCADE)
    local_name = models.CharField(verbose_name="文件（夹）名称", max_length=32, help_text="文件/文件夹")
    file_type = models.SmallIntegerField(verbose_name="类型", choices=((1, "文件"), (2, "文件夹")))
    cos_key = models.CharField(verbose_name="cos文件的key", max_length=128)
    file_path = models.CharField(verbose_name="cos文件的url", max_length=255, null=True, blank=True)
    # https://15885464645-20220417180348-saas-1310871600.cos.ap-chengdu.myqcloud.com/24b921bd6fdb96c737af464d27e0404d.jpg
    parent = models.ForeignKey(verbose_name="父目录", to="FileLibrary", related_name="children", on_delete=models.CASCADE)
    update_user = models.ForeignKey(verbose_name="最近更新者", to="User", on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name="最近更新时间", auto_now=True)
```



## **30.3. 知识点预备：URL传参/不传参**
```python
# URL传参/不传参
path (manage/file/,manage.file，name='fi1e'),
# /file/
# /file/?folder_id=50
def file(request,project_id):
    folder_id = reqeust.GET.get('fo1der_id')
```



## **30.4. 知识点预备：导航条实现思路: 找到父级id，逐级往上寻找，并插入列表第0个位置，直到找到父id为空的**

![img](https://docimg2.docs.qq.com/image/CyLeCgsght-Iiuc0J3-XMg.png?w=1077&h=453)        



```python
def file(request,project_id):
    folder_id = reqeust.GET.get('fo1der_id')
    res_lst = []
    
    if not folder_id:
        pass
    else:
        row_obj = models.FileLibrary.objects.filter(id=folder_id, project=request.tracer.project).first()
        
    while row_obj:  # 直到找到父id为空的对象
        res_lst.insert(0, row_obj)  # 对象1/对象2/对象3
```



## **30.5. 知识点预备：js的SDK前端直接上传cos(注意：密钥安全处理)**

**腾讯云cos JS前端上传文档：**[**https://cloud.tencent.com/document/product/436/11459**](https://cloud.tencent.com/document/product/436/11459)

**解读文档：**



```javascript
<input id="file-selector" type="file">
<script src="dist/cos-js-sdk-v5.min.js"></script>
<script>


// 存储桶名称，由bucketname-appid 组成，appid必须填入，可以在COS控制台查看存储桶名称。 https://console.cloud.tencent.com/cos5/bucket
var Bucket = 'examplebucket-1250000000';  /* 存储桶，必须字段 */


// 存储桶region可以在COS控制台指定存储桶的概览页查看 https://console.cloud.tencent.com/cos5/bucket/ 
// 关于地域的详情见 https://cloud.tencent.com/document/product/436/6224
var Region = 'COS_REGION';     /* 存储桶所在地域，必须字段 */


// 初始化实例
var cos = new COS({
    // getAuthorization 必选参数
    getAuthorization: function (options, callback) {
        // 异步获取临时密钥
        // 服务端 JS 和 PHP 例子：https://github.com/tencentyun/cos-js-sdk-v5/blob/master/server/
        // 服务端其他语言参考 COS STS SDK ：https://github.com/tencentyun/qcloud-cos-sts-sdk
        // STS 详细文档指引看：https://cloud.tencent.com/document/product/436/14048


        var url = 'http://example.com/server/sts.php'; // url替换成您自己的后端服务
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url, true);
        xhr.onload = function (e) {
            try {
                var data = JSON.parse(e.target.responseText);
                var credentials = data.credentials;
            } catch (e) {
            }
            if (!data || !credentials) {
              return console.error('credentials invalid:\n' + JSON.stringify(data, null, 2))
            };
            callback({
              TmpSecretId: credentials.tmpSecretId,
              TmpSecretKey: credentials.tmpSecretKey,
              SecurityToken: credentials.sessionToken,
              // 建议返回服务器时间作为签名的开始时间，避免用户浏览器本地时间偏差过大导致签名错误
              StartTime: data.startTime, // 时间戳，单位秒，如：1580000000
              ExpiredTime: data.expiredTime, // 时间戳，单位秒，如：1580000000
          });
        };
        xhr.send();
    }
});


// 接下来可以通过 cos 实例调用 COS 请求。


</script>
```


##  **30.6. 知识点预备：跨域问题设置**

![img](https://docimg8.docs.qq.com/image/rCmc6GJEPtQeT8HBhcJjNw.png?w=1033&h=87)        **跨域问题原理：**

![img](https://docimg2.docs.qq.com/image/9Fb81fHqSlNNVy_zaTOOFg.png?w=899&h=522)        

**cos设置跨域访问 header (可以通过创建桶的时候 参数设置)：**

![img](https://docimg2.docs.qq.com/image/pdfquBlw4i1wWUkw86ljNA.png?w=855&h=617)        

**python后端实现创建桶并做跨域设置：cos.py设置**



```python
# 创建公有读私有写的桶
def wiki_create_bucket(bucket, acl='public-read'):
    client = initCos()
    response = client.create_bucket(
        Bucket=bucket,
        ACL=acl,
    )


    # 跨域API配置
    cors_config = {
        'CORSRule': [
            {
                'AllowedOrigin': '*',
                'AllowedMethod': ['GET', 'PUT', 'HEAD', 'POST', 'DELETE'],
                'AllowedHeader': "*",
                'ExposeHeader': "*",
                'MaxAgeSeconds': 500
            }
        ]
    }
    
    client.put_bucket_cors(
    Bucket=bucket,
    CORSConfiguration=cors_config,
)
```



##  **30.7. 知识点预备：前端闭包（面试题分享及理解）**



```javascript
JavaScript this 关键字面向对象语言中 this 表示当前对象的一个引用。
但在 JavaScript 中 this 不是固定不变的，它会随着执行环境的改变而改变。
在方法中，this 表示该方法所属的对象。
如果单独使用，this 表示全局对象。
在函数中，this 表示全局对象。
在函数中，在严格模式下，this 是未定义的(undefined)。
在事件中，this 表示接收事件的元素。
类似 call() 和 apply() 方法可以将 this 引用到任何对象。




var name ="全栈28期"
function func(){
var name ="全栈25期"
console.log(name) // 全栈25
}
func();




var name ="全栈28期"
function func(){
	var name ="全栈25期"
	console.log(this.name) //全栈28期
}
func();
等价于： window.func();  //最外层在调用




var name ="王洋"
function func(){
	var name ="全栈25期"
	console.log(this.name) //全栈28期
}
func();




var name ="王洋"
info = {
	name: "陈硕"，
	func:function(){
	    console.log(this.name) //陈硕
	}
}
info.func();




this表示谁在调用它，他就是谁~~~~




var name ="王洋"
info = {
		name:"陈硕"，
		func: function(){
		console.log(this.name) ;//info.name 陈硕
        }
		function test（）{
            console.log(this.name) ;//#window.name >王洋
        }
	}
	test()  //前面没指定，默认为window.test(),这就是最终结果
}
info.func()
```



**Ajax属于异步请求：就是可以在执行未完成前，后面函数先执行，回调函数1分钟之后执行。**



```python
data_list =[11,22,33]
for(var i; i++; i<data.length){l
    //循环会发送三次ajax请求，由于ajax是异步请求，所以在发送请求时候不会等待。
    $.ajax({  //异步执行
        url : ".... ",
        data:{value : data_list[i]}，
        success :function(res){
            //1分钟之后执行回调函数
            console.log(i) //这里每次回调 i=2 因为3次循环已经做完！回调后边做的。 
        }
    });
}
console.log(i)  //瞬间循环完成 i=2；上面回调未开始...
```

 



**对异步Ajax请求使用函数闭包方式，分别按顺序执行函数**



```python
data_list =[11,22,33]
for(var i; i++; i<data.length){
    //循环会发送三次ajax请求，由于ajax是异步请求，所以在发送请求时候不会等待。
   function xx(data){
            $.ajax({  //异步执行
            url : ".... ",
            data:{
                value : data_list[i]]
            }，
            success :function(res){
                //1分钟之后执行回调函数
                console.log(i) //这里每次回调 i=0/1/2
            }
        });
    }
    xx(i) //每次循环创建一块区域运行一次函数
}
console.log(i)  //瞬间循环完成 i=2；上面回调未开始...
```



**上面代码也可以改为自执行函数**



```python
data_list =[11,22,33]
for(var i; i++; i<data.length){
    //循环会发送三次ajax请求，由于ajax是异步请求，所以在发送请求时候不会等待。
   (function xx(data){
            $.ajax({  //异步执行
            url : ".... ",
            data:{
                value : data_list[i]]
            }，
            success :function(res){
                //1分钟之后执行回调函数
                console.log(i) //这里每次回调 i=0/1/2
            }
        });
    })(i) //每次循环创建一块区域运行一次函数
}
console.log(i)  //瞬间循环完成 i=2；上面回调未开始...
```



**注意事项：**



**如果以后，需要循环发送异步请求，异步任务成功后，通过怕闭包解决控制每次函数想要传入的参数数据；**

#  **31. 文件管理列表显示和添加文件夹模态框**

## **31.1. 列表显示：新建按钮 -> modelform -> 展示input框 -> 校验等...**

## **31.2. 知识点：bootstrap模态框的多重应用(data-whatever)**



### **- 初始化绑定的模态框**



```javascript
//初始化-动态应用模态框展示
function initAddModal() {
    $('#addModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var recipient = button.data('whatever'); // Extract info from data-* attributes
        var modal = $(this);
        modal.find('.modal-title').text(recipient);
    });
}
```



### **- 设置属性** data-whatever**= "标题"**



```
<a class="btn btn-success btn-xs" data-toggle="modal" data-target="#addModal" data-whatever="新建文件夹">
    <i class="fa fa-plus-circle" aria-hidden="true"></i> 新建文件夹
</a>
```

 



### **- 实现思路**



```
1\ 在前端展示文件夹是一个a标签，点击携带文件夹的folder_id进入视图函数，以此作为父目录查找；
2\ 视图函数获取folder_id，如果为空，则pass,反之，判断folder_id.isdecimal;
3\ 获取到当前id=folder_id的对象，以此作为父对象；
4\ 如果GET请求，则选出全部parent=获取到的父对象。文件夹排在前面展示在前端；
5\ POST请求，则需要先判断当前目录是否存在同名文件夹，对名称校验，并返回前端ajax回调函数用于展示，注意：要区分当前目录是否为根目录，根目录则其parent_isnull=True
```



### **- 这里只展示对文件是否重名的校验代码**



```
def clean_local_name(self):
    txt_local_name = self.cleaned_data.get("local_name")
    queryset = models.FileLibrary.objects.filter(local_name=txt_local_name, file_type=2, project=self.request.tracer.project)
    # 判断当前项目的文件管理的文件目录下(父id相同)是否存在同名文件夹，当父对象为空，就去查根目录
    exist = None
    if self.parent_obj:
        exist = queryset.filter(parent=self.parent_obj).exists()  # 查询同一个父目录的所有文件
    else:
        exist = queryset.filter(parent__isnull=True).exists()


    if exist:
        raise ValidationError("该目录下已存在同名文件！")
    else:
        pass
    return txt_local_name
```



**前端页面：列表显示文件夹名称可以点击进入，携带相应参数**                 ![img](https://docimg6.docs.qq.com/image/-g7NFFR_rFw0cNZvGtsDhg.png?w=1280&h=573.3250155957579)        

**注意：****当使用POST请求提交到当前访问路径时，前端js直接使用 url: location.href,**



```javascript
function bindSavebtn() {
    $("#savebtn").click(function () {
        $.ajax({
            url: location.href, //提交到当前访问页面地址（附带参数）
            type: "post",
            data: $("#add_form").serialize(),
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    $("#addFolder").modal("hide")
                    $("#smallmodal").modal("show")
                    location.reload(); //页面刷新
                } else {
                    $(".error-msg").text("")
                    $.each(res.errors, function (name, data) {
                        $("#id_" + name).next().text(data[0])
                    })
                }
            },
        });


    });
}
```



#  **32. 实现新建文件夹、文件夹及文件重命名、删除文件或文件夹**

## **32.1. 新建文件夹-思路**



```
1\ 新建文件夹按钮，绑定事件点击则显示模态框，form表单显示；填入表单；
2\ 提交表单，验证处理，处理当前文件或文件夹所在目录的对应关系，做好未显示的表单初始化处理；
```

集成到列表展示，以及导航处理
**相关代码：**



```
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
        objs = models.FileLibrary.objects.filter(project=request.tracer.project,parent=parent_obj).order_by("-file_type")
        context = {
            "form": form,
            "objs": objs,
            "result_lst": result_lst
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
```


## **32.2. 编辑文件/文件夹-思路**



```tex
1\ 编辑按钮绑定文件/文件夹的id，点击获取到对应id，在后端请求获取获取当前数据行，再打开模态框，将数据初始化到对应
的form表单，再用js手动打开模态框（非直接绑定按钮），填入对应数据展示；
2\ 用户填入数据，提交表单，相当于再次提交，注意实例化modelform采用instance参数，否则就会重新创建，而不是替换数据；
3\ 需要考虑当前修改的是文件还是文件夹，做不同的处理；
```





**前端相关代码：**



```javascript
var FEXT; //编辑文件的后缀
var EDIT_FID; //编辑按钮绑定的fid
var EDIT_PID; //编辑按钮绑定的pid
var FIRST_NAME;  //编辑文件或文件夹的名称(不含后缀)
var EDIT_GETDATA_URL = "{% url 'file_edit_getdata' project_id=request.tracer.project.id %}";
var EDIT_URL = "{% url 'file_edit' project_id=request.tracer.project.id %}";
var DELETE_URL = "{% url 'file_delete' project_id=request.tracer.project.id%}";


//点击编辑，get请求获取数据前端显示
function bindEditbtn() {
    $(".edit_btn").click(function () {
        //编辑的时候设置的属性
        EDIT_FID = $(this).attr("fid");
        EDIT_PID = $(this).attr("pid");
        var local_name = $(this).attr("local_name");
        //获取最后一个.的位置
        var index = local_name.lastIndexOf(".");
        if (index === -1) { //判断是否含有”.“，没有返回-1，区别是文件还是文件夹
            FEXT = "";
            FIRST_NAME = local_name;
        } else {
            //获取后缀,存入全局变量
            FEXT = local_name.substr(index + 1);
            //获取不含后缀名称
            FIRST_NAME = local_name.substring(0, local_name.lastIndexOf("."));
        }
        //console.log(FIRST_NAME);
        $.ajax({
            url: EDIT_GETDATA_URL,   //get请求提交地址
            type: 'get',
            data: {
                fid: EDIT_FID //get请求 参数:值
            },
            dataType: 'JSON',
            //POST请求成功返回数据
            success: function (res) {
                if (res.status) {
                    // console.log(res)
                    //清空错误提示
                    $(".error-msg").text("");
                    // 清空模态框表单
                    $("#myform")[0].reset();
                    // 利用标签设置标题
                    $(".modal-title").text("编辑文件/文件夹");
                    // 循环以id_name填入数据
                    $.each(res.data, function (name, value) {
                        if (name === "local_name") {
                            $("#id_local_name").val(FIRST_NAME);
                        } else {
                            $("#id_" + name).val(value);
                        }
                    })
                    // 最后展示模态框
                    $("#myModal").modal("show");


                } else {
                    alert(res.error)
                }
            },
        });
    })
}


//编辑提交数据
function doEdit() {
    $.ajax({
        url: EDIT_URL + "?folder_id=" + EDIT_PID + "&fid=" + EDIT_FID + "&fext=" + FEXT,  //编辑路径,注意顺序以及多个参数写法
        type: 'post',
        dataType: "JSON",
        data: $("#myform").serialize(),
        success: function (res) {
            if (res.status) {
                $("#myModal").modal("hide");
                $("#smallmodal").modal("show");
                setTimeout("location.reload()", 888);
            } else {
                $.each(res.errors, function (name, data) {
                    $("#id_" + name).next().text(data[0]);
                })
            }
            console.log(res)
        }
    })
}
```





 

## **32.3. 删除文件/文件夹-思路**



```tex
1\ 数据库删除：删除绑定id的文件或文件夹，自动级联删除；
2\ cos删除：需要考虑当前删除的文件夹下所有的文件或更深层下去的文件；逐级查找，
```

 **知识点：当上向下逐级查找，使用列表一边元素循环，一边元素增加，示例如下：**



```
lst1 = [[1,2,3,4,5], ]


for i in lst1:
    lst1.append(i)
    if len(lst1) == 5:
        break


print(lst1) #[[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
```

 

**代码实现**



```
if delete_obj:
    # 1.数据库删除,归还用户存储空间
    delete_obj.delete()
    delete_obj.project.used_space -= delete_obj.file_size
    delete_obj.project.save()  # 直接保存到数据库


    # 2.cos删除
    key_list = []
    total_size = 0
    if delete_obj.file_type == 1:  # 文件
        cos.cos_delete_object(bucket=delete_obj.project.bucket, key=delete_obj.key)
    else:  # 文件夹，删除所有以他为父目录的文件或文件夹，逐级删除, 一边循环元素，一边判断添加元素
        folder_objs = [delete_obj, ]
        for folder in folder_objs:
            child_objs = models.FileLibrary.objects.filter(parent=folder, project=request.tracer.project).order_by("-file_type")
            for child in child_objs:
                if child.file_type == 2:
                    folder_objs.append(child_obj)
                else:  # 文件
                    total_size += child.file_size  # 文件大小汇总
                    # cos删除文件
                    key_list.append([{"key": child.cos_key}])
        # 执行cos文件删除
        cos.cos_delete_objects(bucket=request.tracer.project.bucket, key_list=key_list)
```


#  **33. 上传文件**



```
1\ 上传文件按钮样式处理，
2\ 按钮绑定事件，点击选择文件，change事件，在点击后获取文件确定后自动触发，获取临时凭证上传文件，
```


## **上传文件按钮设置样式（默认样式丑！）**

**HTML: 需要支持多选，input file增加** **multiple**



```html
<!--右边显示-->
<div class="col-md-6 text-right uploadcss">
    <div class="btn btn-primary btn-xs upload">
        <div><i class="fa fa-upload" aria-hidden="true"></i> 上传文件</div>
        <input type="file" multiple name="uploadFile" id="uploadFile">
    </div>
    <button class="btn btn-success btn-xs" id="add_btn">
        <i class="fa fa-plus-circle" aria-hidden="true"></i> 新建文件夹
    </button>
</div>
```

 **CSS**

 

```css
/*文件上传*/
.uploadcss .upload {
    overflow: hidden;
    position: relative
}


.uploadcss .upload input {
    opacity: 0;
    position: absolute;
    top: 0;
    bottom: 0;
    width: 76px;
    left: -2px;
    overflow: hidden;
}
```

![img](https://docimg9.docs.qq.com/image/iz5hWGXsmDtUgJK5iJvutg.png?w=1008&h=343)        



# **34. 上传文件实现**

## **34.1. 知识点：为什么jquery对象需要转化为DOM对象?**



```
jQuery对象和DOM对象都是获取到的页面节点对象，为什么还需要相互转化呢？
原因是在 jQuery 对象中无法使用 DOM 对象的任何方法，如 $(“p”).innerHtml 是错误的，因为它的写法是 $(“p”).html()。同样，DOM对象中也不能用 jQuery 对象中的方法，如 document.getElementsByTagName(“p”).html() 是错误的。
```





**详细解释：**

[**jQuery对象与DOM对象的相互转化**](https://blog.csdn.net/Erudite_x/article/details/117450388) 

[**File 对象，FileList 对象，FileReader 对象**](https://wangdoc.com/javascript/bom/file.html)

**所以转化之后，使用DOM中的.files方法获取到上传文件信息对象，（类似字典）**



**示例：打印上传文件列表**



```
//文件上传
function binduploadFile() {
    $("#uploadFile").change(function () {
        var fileList = $(this)[0].files;
        $.each(fileList, function (index, fileObject) {
            console.log(index, fileObject)
        })
    })
}
```

![img](https://docimg9.docs.qq.com/image/-_Ua8ZUIFzdsJDRXfxi3ow.png?w=1280&h=464.01880141010577)



## **34.2. 结合cos上传文件**



```
1\ 获取临时品凭证；
2\ 右下角展示进度条；
3\ 上传文件保存到数据库；
4\ 容量限制；
```

 



- **获取临时凭证**

- **知识点：**XMLHttpRequest() , XMLHttpRequest 可以在不刷新页面的情况下请求特定 URL，获取数据。



```
XMLHttpRequest参数提交方式


一般情况下，使用Ajax提交的参数多是些简单的字符串，可以直接使用GET方法将要提交的参数写到open方法的url参数中，此时send方法的参数为null。
例如 ：


var url = "login.jsp?user=XXX&pwd=XXX";
xmlHttpRequest.open("GET",url,true);
xmlHttpRequset.send(null);
 
此外，也可以使用send方法传递参数。使用send方法传递参数使用的是POST方法，需要设定Content-Type头信息，模拟HTTP POST方法发送一个表单，这样服务器才会知道如何处理上传的内容。
参数的提交格式和GET方法中url的写法一样。设置头信息前必须先调用open方法。例如：


xmlHttpRequest.open("POST","login.jsp",true);
// xmlHttpRequest.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
xmlHttpRequest.setRequestHeader("Content-Type","application/json;charset=UTF-8");
xmlHttpRequest.send("user="+username+"&pwd="+password);
```

 



- 深入学习XMLHttpRequest https://developer.mozilla.org/zh-CN/docs/conflicting/web/api/xmlhttprequest/load_event
- Content-Type详解：https://blog.csdn.net/qq_14869093/article/details/86307084  就是发送数据到后端的形式



```
//文件上传
function binduploadFile() {
    $("#uploadFile").change(function () {
        // 上传之前初始化获取临时凭证
        var cos = new COS({
            // getAuthorization 必选参数
            getAuthorization: function (options, callback) {
                // 异步获取临时密钥
                var url = CREDENTIAL_URL; // url替换成您自己的后端服务
                var xhr = new XMLHttpRequest();
                xhr.open('POST', url, true);
                xhr.onload = function (e) {
                    // console.log(JSON.parse(e.target.responseText).data.credentials)
                    try {
                        var data = JSON.parse(e.target.responseText).get_data; //数据转换，对象获取数据
                        var credentials = data.credentials;
                    } catch (e) {
                    }
                    if (!data || !credentials) {
                        return console.error('credentials invalid:\n' + JSON.stringify(data, null, 2))
                    }
                    callback({
                        TmpSecretId: credentials.tmpSecretId,
                        TmpSecretKey: credentials.tmpSecretKey,
                        SecurityToken: credentials.sessionToken,
                        // 建议返回服务器时间作为签名的开始时间，避免用户浏览器本地时间偏差过大导致签名错误
                        StartTime: data.startTime, // 时间戳，单位秒，如：1580000000
                        ExpiredTime: data.expiredTime, // 时间戳，单位秒，如：1580000000
                    });
                };
                xhr.send();
            }
        });


        //获取临时凭证：5秒时效
        var fileList = $(this)[0].files;
        $.each(fileList, function (index, fileObject) {
            console.log(index, fileObject);
            //循环上传文件，异步提交
            cos.putObject({
                Bucket: "{{ request.tracer.project.bucket }}", /* 必须 */
                Region: "{{ request.tracer.project.region }}", /* 存储桶所在地域，必须字段 */
                Key: fileObject.name, /* 必须：文件name */
                StorageClass: 'STANDARD',  /* 非必须：动态扩容 */
                Body: fileObject, // 上传文件对象
                onProgress: function (progressData) {
                    console.log("文件上传进度-->", JSON.stringify(progressData)); //上传进度
                }
            }, function (err, data) {
                console.log(err || data);
            });


        })


    })
}
```





- **后端服务**



```
# 前端获取cos临时凭证上传文件
def upload_credential(bucket, region, secret_id=settings.COS_SECRET_ID, secret_key=settings.COS_SECRET_KEY):
    config = {
        'url': 'https://sts.tencentcloudapi.com/',
        # 域名，非必须，默认为 sts.tencentcloudapi.com
        'domain': 'sts.tencentcloudapi.com',
        # 临时密钥有效时长，单位是秒
        'duration_seconds': 30,
        'secret_id': secret_id,
        # 固定密钥
        'secret_key': secret_key,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        'bucket': bucket,
        # 换成 bucket 所在地区
        'region': region,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        'allow_prefix': '*',
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        'allow_actions': [
            "*",
            # # 简单上传
            # 'name/cos:PutObject',
            # 'name/cos:PostObject',
            # # 分片上传
            # 'name/cos:InitiateMultipartUpload',
            # 'name/cos:ListMultipartUploads',
            # 'name/cos:ListParts',
            # 'name/cos:UploadPart',
            # 'name/cos:CompleteMultipartUpload'
        ],
    }


    try:
        sts = Sts(config)
        result_dict = sts.get_credential()  # 字典类型数据
        return result_dict
    except Exception as e:
        print(e)
```







```
# 视图函数
def file_cos(request, project_id):
    """获取cos临时凭证"""
    result_dict = cos.upload_credential(bucket=request.tracer.project.bucket, region=request.tracer.project.region)
    return JsonResponse({'status': True, 'get_data': result_dict})
```





**注意：函数参数一定要写入括号内，不然不被识别**

![img](https://docimg9.docs.qq.com/image/QTnHZF4E9qrey4dgjDko5g.png?w=1280&h=363.2676056338028)    



## **34.3. 文件上传限制**



```
1\ 获取临时凭证的时候，做判断；
2\ 单文件不能超过5M，注意单位：价格策略里面为MB，存入数据库为字节；
3\ 传入文件+已使用空间不能大于单项目最大限制空间；
4\ 注意ajax： var xhr = new XMLHttpRequest(); 这样### **文件上传进度条处理（前端知识）**



```

```tex
1\ 创建显示面板，最初为隐藏状态，上传文件时显示出来；
2\ 样式里面显示在屏幕右下角，css样式设置；
3\ 里面装表格，一条数据就是一个文件进度，做一个模板，循环上传时，模板加到指定的位置
var tr = $("#progressTemplate").find("tr").clone() //获取模板中的tr
tr.find(".name").text(filename) //找到类为name的div填入文件名称
$("#progressList").append(tr) //一条tr加到进度面板
tr.find(".progress-bar").css("width", percent) //更改width样式
4\ 获得凭证成功后，显示进度面板
//授权通过展示移除进度显示隐藏类
$("#uploadProgress").removeClass("hide")
```



**动态添加按钮无法触发事件：on事件：**

**click例子**



```
$('父元素').on('click', '子元素', function(){})
```



 **父元素为append的元素 ...**

[**https://blog.csdn.net/qq_35129893/article/details/78363211?locationNum=2&fps=1**](https://blog.csdn.net/qq_35129893/article/details/78363211?locationNum=2&fps=1)

![img](https://docimg1.docs.qq.com/image/j7RpPeLaI1JAKPFeGxT8SA.png?w=1280&h=756.67107001321)        



### **文件上传成功之后，文件信息存入数据库**



```
1\ 每个文件成功上传cos后会有回调函数，在回调函数会返回存入的文件相关信息如：ETag，statusCode等；
2\ 由此，在回调函数中，我们可以再用ajax 发送post请求 将文件相关信息，以及ETag给后端服务，利用ETag对将要存入数据库的数据进行校验（防止post发送了一个没有存入cos的文件名到数据库，也就是每次发送的ETag在后天暂存，再去cos查文件的ETag，两个进行比对，不存在则post发送的文件信息不存到数据库！
3\ 存入后，项目已使用空间需要加上存入项目中的文件的大小，（不需要校验超限，超限已在获取凭证时做过）
```

 **流程原理**



![img](https://docimg5.docs.qq.com/image/_FyFB4gm2VvghmLg6cvp5Q.png?w=1052&h=483)        

**Ajax发送post请求,后端ModelForm对数据接受校验：**



```
//前端文件名的处理
... ...
var suffix;
var filename = fileObject.name
var index_num = filename.lastIndexOf("."); //获取最后一个.的位置


//文件名过长处理
if (index_num !== -1 && filename.length > 32) { //判断是否含有”.“，没有返回-1，文件本身不含后缀


    suffix = filename.substr(index_num + 1);
    var firstname = filename.substring(0, 32 - suffix.length - 1)  //文件名长度最多32位处理
    filename = firstname + "." + suffix
} else {
    filename = filename;
}
... ...
```

 **后端数据接收，表单验证：**





```
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
... ...


@csrf_exempt
def file_post(request, project_id):
    """上传成功一个创建一个数据到数据库"""
    # 结合ModelForm进行数据校验
    # print(request.POST)  # 表单数据 queryDict:...
    form = CheckFileModelForm(request, data=request.POST)  # 校验model
    if form.is_valid():
        form.instance.file_type = 1
        form.instance.project = request.tracer.project
        form.instance.update_user = request.tracer.user
        instence = form.save()
        # 项目已使用空间需要增加（不需要再校验空间是否已满，获取凭证已做过）
        # request.tracer.project.used_space += int(request.POST.get("file_size"))  # 此写法针对单线程可以，多线程就会有问题
    # request.tracer.project.save()  # 保存到数据库
    request.tracer.project.used_space = F("used_space") + data_dict["file_size"]  # 多post请求，多线程并发资源竞争问题解决方法(以后就这样写法)
request.tracer.project.save()    
        
        
        if not instence.parent:
            pid = None
        else:
            pid = instence.parent.id


        # 返回给前端显示当前添加的行数据
        show_data = {
            "fid": instence.id,
            "pid": pid,
            "local_name": instence.local_name,
            "file_size": instence.file_size,
            "update_user": instence.update_user.username,
            "update_time": instence.update_time.strftime("%Y年%#m月%d日 %H:%M"),
            # "update_time": datetime.datetime.strftime(instence.update_time, "%Y年%-m月%d日 %H:%M"),
        }


        return JsonResponse({"status": True, "show_data": show_data})
    else:
        return JsonResponse({"status": False, "errors": form.errors})


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
```

**时间月份前面去除0（去除前导）  # 号设置即可 ：** "%Y年%#m月%d日 %H:%M"





#  **35. 下载文件**

## **35.1. 文件的传输本质：文件传输就是二进制数据传输。**

```
浏览器	django
请求	HttpResponse	(...)文本;响应头
请求	render			(...)文本;响应头
请求	...				文件内容;响应头
```

## **35.2. 本地文件下载**
```python
def download():
    local_name = xxx.png
    with open (local_name, mode="rb",encoding="utf-8") as f:
        data = f.read("") #文件内容


    response = HttpResponse(data)  
    # 设置响应头 response["x"] = "值"
    # 设置响应头：中文文件名转义escape_uri_path模块
    from django.utils.encoding import escape_uri_path
    response['Content-Disposition'] = "attachment; filename={};".format(escape_uri_path(file_object.local_name))
    return response
```

 



**cos文件支持下载**

```
import requests  # 文件下载分块处理方法
from django.utils.encoding import escape_uri_path


def file_download(request, project_id, fid):
    """ 下载文件 """


    file_object = models.FileLibrary.objects.filter(id=fid, project=request.tracer.project).first()
    # 文件分块处理（适用于大文件）
    res = requests.get(file_object.file_path)  # 获取cos文件内容
    data = res.iter_content()


    # 设置content_type=application/octet-stream 用于提示下载框
    response = HttpResponse(data, content_type="application/octet-stream")


    # 设置响应头：中文文件名转义
    response['Content-Disposition'] = "attachment; filename={};".format(escape_uri_path(file_object.local_name))
    return response
```

 



#  **35. 第三期项目结束-删除项目（删除cos桶，在删除数据库项目信息）**



```
1\ 删除项目，就先删除桶：删除桶就先删除里面的文件和分块上传未完成产生的碎片；
2\ 删除文件对象及碎片对象：获取对象列表，传入数据删除，对象列表数据[{"Key"："file_name1"},{"Key"："file_name2"}...]
3\ 默认显示当前项目，当前也可以输入其他项目名称，对输入的项目名称校验，是否可以操作，不可以直接返回错误信息！
4\ 删除服务未完成前窗口冻结提示，完成后显示操作成功跳转项目列表页面！
```



**cos代码**


# **35.1 实现删除桶**
```
def cos_delete_bucket(bucket):
    client = initCos()

    if not cos_bucket_exists(bucket):
        return False


    else:
        # 删除正常上传的对象
        while True:
            # 每次最多只能取1000个对象
            part_objects = client.list_objects(Bucket=bucket)


            # 删除Contents的多个对象


            if "Contents" not in part_objects.keys():  # 桶中无文件
                break


            client.delete_objects(
                Bucket=bucket,
                Delete={
                    'Quiet': 'true',
                    'Object': [{"Key": iterm["Key"]} for iterm in part_objects["Contents"]]  # 构造数据格式
                }
            )


            # 判断取到的是否截断（不满1000个对象）
            if part_objects['IsTruncated'] == "false":
                break


        # 删除正在分块上传未完成产生的碎片
        while True:
            # 获取Bucket中正在进行的分块上传的碎片，每次最多只能取1000个
            part_uploads = client.list_multipart_uploads(bucket)


            if 'Upload' not in part_uploads.keys():
                break


            for item in part_uploads['Upload']:
                client.abort_multipart_upload(bucket, item['Key'], item['UploadId'])


            if part_uploads['IsTruncated'] == "false":
                break


        # 完成删除文件与碎片后删除桶
        client.delete_bucket(
            Bucket=bucket
        )


        return True
```







# **36. 第四期项目开始-问题追踪日志**

##  **36.1. 基本思路**



```
1\ 功能基本理解与思路；
2\ 数据库表结构设计；
3\ 前端界面大致样式，根据自己是否能显示？
4\ 分页插件的应用，如何在其中插入，主要考虑尾页新增提交后跳转到尾页或者前端处理直接显示出来（这就应用到之前学的标签内部插入标签，并且设置属性，样式等）。
```







##  **36.2. 数据表结构设计**



```
产品经理：功能 + 原型图
开发人员：设计表结构+代码实现
```





- **功能 + 原型图**

![img](https://docimg10.docs.qq.com/image/905lp95QNsJqhnFELsP0lg.png?w=1280&h=608.7804878048781)        

- **问题表结构设计**
- **class Issue(models.Model):**

| **id** | **title** | **issue_type** | **desc** | **module_title** | **status** | **priority** | **receiver** | **follower**  | **start_time** | **end_time** | **mode** | **pattern** | **creator** | **creat_time** | **update_time**  |
| ------ | --------- | -------------- | -------- | ---------------- | ---------- | ------------ | ------------ | ------------- | -------------- | ------------ | -------- | ----------- | ----------- | -------------- | ---------------- |
| **ID** | **标题**  | **类型FK**     | **描述** | **模块FK**       | **状态CH** | **优先级CH** | **接收者FK** | **关注者m2m** | **开始时间**   | **结束时间** | **模式** | **父问题**  | **创建者**  | **创建时间**   | **最近更新时间** |
|        |           |                |          |                  |            |              |              | 多对多        |                |              |          |             |             |                |                  |



- **class IssueModule(models.Model):**

| **id** | **module_title**     | **project**    |
| ------ | -------------------- | -------------- |
| **ID** | **模块名称**         | **所属项目FK** |
|        | **第一期：用户认证** |                |
|        | **第二期：任务管理** |                |
|        | **第三期：支付模块** |                |



- **class IssueType(models.Model):**

| **id** | **issue_type** | **project**    |
| ------ | -------------- | -------------- |
| **ID** | **类型**       | **所属项目FK** |
|        | **Bug**        |                |
|        | **功能**       |                |
|        | **任务**       |                |



##  **36.3. 前端基础样式**

![img](https://docimg2.docs.qq.com/image/25-9xbfYg3j16yFgzkRQDg.png?w=1280&h=320.6666666666667)        



```
{% extends "web/tpls/manage.html" %}


{% block css %}
*issue模块*/
.issues-list .number {
    width: 100px;
    text-align: right;
}


.issues-list .number a {
    font-weight: 500;
    padding: 0 10px;
}


.issues-list .issue .tags {
    padding: 10px 0;
}


.issues-list .issue .tags span {
    margin-right: 20px;
    display: inline-block;
    font-size: 12px;
}


.issues-list .issue .tags .type {
    color: white;
    padding: 1px 5px;
    margin-left: -3px;
    border-radius: 5px;
    background-color: #dddddd;
}


.pd-0 {
    padding: 0 !important;
}


/* 筛选 */
.filter-area .item {
    margin-bottom: 15px;
}


.filter-area .item .title {
    padding: 5px 0;
}


.filter-area .item .check-list a {
    text-decoration: none;
    display: inline-block;
    min-width: 65px;
}


.filter-area .item .check-list label {
    font-weight: 200;
    font-size: 13px;
    margin-left: 3px;
}


.filter-area .item .check-list a:hover {
    font-weight: 300;
}


.filter-area .item .check-list .cell {
    margin-right: 10px;
}
{% endblock %}




{% block content %}
    <div class="container-fluid" style="padding: 20px 0;">
        <div class="col-sm-3">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <i class="fa fa-search" aria-hidden="true"></i> 筛选
                </div>
                <div class="panel-body filter-area">
                    筛选选项
                </div>
            </div>
        </div>


        <div class="col-sm-9">
            <div class="panel panel-default">
                <div class="panel-heading">
                    <i class="fa fa-quora" aria-hidden="true"></i> 问题
                </div>


                <div class="panel-body">
                    <a class="btn btn-success btn-sm add_btn" style="margin: 10px;">新建问题</a>
                    <a class="btn btn-primary btn-sm invite_btn" style="margin: 10px 0;">邀请成员</a>
                </div>


                <table class="table">
                    <tbody class="issues-list">
                    <tr>
                        <td class="number text-danger">
                            <i class="fa fa-circle"></i>
                            <a target="_blank" href="#">#0134</a>
                        </td>


                        <td class="issue">
                            <div>
                                <a target="_blank" href="#">任务</a>
                            </div>
                            <div class="tags">
                                <span class="type">
                                    功能
                                </span>


                                <span>
                                    <i class="fa fa-refresh" aria-hidden="true"></i> 状态
                                </span>


                                <span>
                                    <i class="fa fa-hand-o-right" aria-hidden="true"></i> 接收者
                                </span>


                                <span>
                                    <i class="fa fa-user-o" aria-hidden="true"></i> 创建者
                                </span>


                                <span>
                                    <i class="fa fa-calendar" aria-hidden="true"></i> 截止时间
                                </span>


                                <span>
                                    <i class="fa fa-clock-o" aria-hidden="true"></i> 最近更新时间
                                </span>
                            </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>


            <nav aria-label="Page navigation">
                <ul class="pagination" style="margin-top: 0">
                    <li>
                        <a href="#" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    <li><a href="#">1</a></li>
                    <li><a href="#">2</a></li>
                    <li><a href="#">3</a></li>
                    <li><a href="#">4</a></li>
                    <li><a href="#">5</a></li>
                    <li>
                        <a href="#" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                </ul>
            </nav>


        </div>
    </div>
{% endblock %}
```







##  **36.4. 新建按钮功能**

- 模态框实现 mdedit 在模态框中全屏显示问题未解决，待寻找方法.... 目前让全屏按钮不显示

![img](https://docimg1.docs.qq.com/image/5Oq_gYXRR-wKzrZzsvFCCw.png?w=1280&h=619.3333333333334)        

- **实现步骤：**

 **前端样式... ...**

 **时间选择器：bootstrap-datatimepicker css\js 引入 & 下拉选择器：bootstrap-selectpicker css\js 引入：** **https://docs.qq.com/doc/DWGZqVmlSeWlmd2FC?u=1311395492be438887a81301175a5f13**



 





##  **36.5. 下拉框显示处理及数据初始化**

**Django-ORM values、values_list区别**



```
# **36. values 结果为字典型**
books = Book.objects.filter(id__lt=6).values('number')
[{'number': '1'}, {'number': '2'}, {'number': '3'}, {'number': '4'}, {'number': '5'}]

# **37. values_list 结果为元祖型**
books = Book.objects.values_list('number')
[('1',), ('2',), ('3',), ('4',), ('5',)]

# **38. 获取某个字段所有值2**
books = Book.objects.values_list('number', flat=True)
books = ['1', '2', '3', '4', '5']

# **39. 获取某个字段所有值（不重复）**
models = Book.objects.filter(group=group).values('number').distinct().order_by('number') #必须有order_by
```

 



##  **36.6. 创建项目对问题类型的初始化**

**ORM初始化列表：**



```
class IssueType(models.Model):
    """问题所属类型表"""


    class Meta:
        verbose_name = '问题类型'  # 设置admin页面右边标题显示
        verbose_name_plural = '问题类型'  # 设置admin页面左边导航显示


        # 设置后台显示信息


    def __str__(self):
        return str(self.title)


    PROJECT_INIT_LIST = ["任务", "功能", "Bug"]
    title = models.CharField(verbose_name="类型名称", max_length=32)
    project = models.ForeignKey(verbose_name="所属项目", to=Project, on_delete=models.CASCADE)
```

 



**批量创建数据行语法：.**objects**.**bulk_create



```
# **40. 初始化当前项目默认问题类型**
objs_list = []
for item in models.IssueType.PROJECT_INIT_LIST:
    print(models.IssueType(title=item, project=instance))
    objs_list.append(models.IssueType(title=item, project=instance))
models.IssueType.objects.bulk_create(objs_list)  # 批量添加数据行
```