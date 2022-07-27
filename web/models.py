# -*- coding=utf-8
from django.db import models


class User(models.Model):
    """用户信息"""

    class Meta:
        verbose_name = '普通用户'  # 设置admin页面右边标题显示
        verbose_name_plural = '普通用户'  # 设置admin页面左边导航显示

    # 设置后台显示信息
    def __str__(self):
        return self.username

    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', max_length=64)
    phone = models.CharField(verbose_name='手机号码', max_length=11)


class PricePolicy(models.Model):
    """价格策略"""

    class Meta:
        verbose_name = '价格策略'  # 设置admin页面右边标题显示
        verbose_name_plural = '价格策略'  # 设置admin页面左边导航显示

    # 设置后台显示信息
    def __str__(self):
        return self.get_tos_display()

    choice = (
        (1, "免费版"),
        (2, "收费版"),
        (3, "其他")
    )
    tos = models.SmallIntegerField(verbose_name="业务类型", choices=choice, default=2)  # 默认购买后自动变为2
    level = models.CharField(verbose_name="业务级别", max_length=16)
    price = models.PositiveIntegerField(verbose_name="价格/年")  # 大于等于0的整数类型
    project_num = models.PositiveIntegerField(verbose_name="项目创建数量上限")
    member_num = models.PositiveIntegerField(verbose_name="项目参与成员上限")
    project_space = models.PositiveIntegerField(verbose_name="项目空间上限", help_text="G")
    up_filesize = models.PositiveIntegerField(verbose_name="单个文件上传大小限制", help_text="M")
    # 添加数据行时自动创建时间为系统当前时间
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Deal(models.Model):
    """交易记录"""

    class Meta:
        verbose_name = '交易记录'  # 设置admin页面右边标题显示
        verbose_name_plural = '交易记录'  # 设置admin页面左边导航显示

    # 设置后台显示信息
    def __str__(self):
        return self.order_num

    choice = (
        (1, "待支付"),
        (2, "已支付")
    )
    status = models.SmallIntegerField(verbose_name="交易状态", choices=choice)
    order_num = models.CharField(verbose_name="订单号", max_length=64, unique=True)  # unique唯一索引
    trader = models.ForeignKey(verbose_name="交易者", to="User", on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name="价格策略", to="PricePolicy", default=0, on_delete=models.CASCADE)  # 价格策略
    payment = models.PositiveIntegerField(verbose_name="实际支付")
    year_num = models.IntegerField(verbose_name="购买数量（年）", help_text='0表示无限期')
    start = models.DateTimeField(verbose_name="业务开始时间", null=True, blank=True)
    end = models.DateTimeField(verbose_name="业务结束时间", null=True, blank=True)
    creat_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class Project(models.Model):
    """项目信息(项目-用户关系1V1)"""

    class Meta:
        verbose_name = '项目信息'  # 设置admin页面右边标题显示
        verbose_name_plural = '项目信息'  # 设置admin页面左边导航显示

    # 设置后台显示信息
    def __str__(self):
        return self.project_name

    color_choice = (
        (1, "#56b8eb"),  # 56b8eb
        (2, "#f28033"),  # f28033
        (3, "#ebc656"),  # ebc656
        (4, "#a2d148"),  # a2d148
        (5, "#20BFA4"),  # #20BFA4
        (6, "#7461c2"),  # 7461c2,
        (7, "#20bfa3"),  # 20bfa3,
    )
    project_name = models.CharField(verbose_name="项目名称", max_length=32)
    color = models.SmallIntegerField(verbose_name="显示颜色", choices=color_choice, default=1)
    desc = models.CharField(verbose_name="项目描述", max_length=2000)
    star = models.BooleanField(verbose_name="星标", default=False)
    member_num = models.PositiveIntegerField(verbose_name="参与人数", default=1)
    creator = models.ForeignKey(verbose_name="创建者", to="User", on_delete=models.CASCADE)
    used_space = models.PositiveIntegerField(verbose_name="项目已使用空间", default=0, help_text='字节')
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    bucket = models.CharField(verbose_name="cos桶", max_length=128)
    region = models.CharField(verbose_name="cos区域", max_length=32)


class ProjectUser(models.Model):
    """项目参与(项目-用户关系nVn)"""

    class Meta:
        verbose_name = '项目参与'  # 设置admin页面右边标题显示
        verbose_name_plural = '项目参与'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.project)

    project = models.ForeignKey(verbose_name="项目信息", to="Project", max_length=32, on_delete=models.CASCADE)
    participant = models.ForeignKey(verbose_name="参与者", to="User", on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name="星标", default=False)
    create_time = models.DateTimeField(verbose_name="加入时间", auto_now_add=True)


class Wiki(models.Model):
    """wiki目录表"""

    class Meta:
        verbose_name = 'wiki文章'  # 设置admin页面右边标题显示
        verbose_name_plural = 'wiki文章'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.title)

    title = models.CharField(verbose_name="标题", max_length=32)
    content = models.TextField(verbose_name="内容")
    project = models.ForeignKey(verbose_name="项目信息", to="Project", on_delete=models.CASCADE)
    # 自关联，最好设置反向关联别名，否则由于本身也关联，外部也来反向关联可能会有问题。
    parent = models.ForeignKey(verbose_name="父文章", to="Wiki", null=True, blank=True, related_name="child", on_delete=models.CASCADE)
    depth = models.PositiveIntegerField(verbose_name="深度", default=0)


class FileLibrary(models.Model):
    """wiki信息表"""

    class Meta:
        verbose_name = '文件仓库'  # 设置admin页面右边标题显示
        verbose_name_plural = '文件仓库'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.local_name)

    INIT_FOLDERS = ["我的文档", "我的图片", "我的视频", "我的音频"]

    project = models.ForeignKey(verbose_name="项目信息", to="Project", on_delete=models.CASCADE)
    local_name = models.CharField(verbose_name="名称", max_length=32, help_text="文件或文件夹名称")
    file_size = models.PositiveIntegerField(verbose_name="大小", default=0, help_text="字节")
    file_type = models.SmallIntegerField(verbose_name="类型", choices=((1, "文件"), (2, "文件夹")), help_text="文件或文件夹")
    cos_key = models.CharField(verbose_name="cos文件的key", max_length=128, null=True, blank=True)
    file_path = models.CharField(verbose_name="cos文件的url", max_length=255, null=True, blank=True)
    # https://15885464645-20220417180348-saas-1310871600.cos.ap-chengdu.myqcloud.com/24b921bd6fdb96c737af464d27e0404d.jpg
    parent = models.ForeignKey(verbose_name="父目录", to="FileLibrary", related_name="child", on_delete=models.CASCADE, null=True, blank=True)
    update_user = models.ForeignKey(verbose_name="最近更新者", to="User", on_delete=models.CASCADE)
    update_time = models.DateTimeField(verbose_name="最近更新时间", auto_now=True)


class Issue(models.Model):
    """问题信息表"""

    class Meta:
        verbose_name = '问题追踪'  # 设置admin页面右边标题显示
        verbose_name_plural = '问题追踪'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.title)

    status_choices = (
        (1, "新建"),
        (2, "处理中"),
        (3, "已解决"),
        (4, "已忽略"),
        (5, "待反馈"),
        (6, "已关闭"),
        (7, "问题重启"),
    )

    priority_choices = (
        ("danger", "高"),
        ("warning", "中"),
        ("success", "低"),
    )

    mode_choices = (
        (1, "公开模式"),
        (2, "隐私模式"),
    )

    title = models.CharField(verbose_name="主题", max_length=64)
    issue_type = models.ForeignKey(verbose_name="类型", to="IssueType", on_delete=models.CASCADE)
    desc = models.TextField(verbose_name="描述")
    module = models.ForeignKey(verbose_name="模块", to="IssueModule", on_delete=models.CASCADE, null=True, blank=True)
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    priority = models.CharField(verbose_name="优先级", choices=priority_choices, default="danger", max_length=32)
    receiver = models.ForeignKey(verbose_name="接收者", to="User", related_name="issue_receiver", null=True, blank=True, on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name="关注者", to="User", related_name="issue_follower", null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    mode = models.SmallIntegerField(verbose_name="模式", choices=mode_choices, default=1)
    parent = models.ForeignKey(verbose_name="父问题", to="Issue", related_name="child", null=True, blank=True, on_delete=models.CASCADE)
    creator = models.ForeignKey(verbose_name="创建者", to="User", related_name="issue_creator", on_delete=models.CASCADE)
    creat_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)  # 添加的数据自动设置当前时间
    update_time = models.DateTimeField(verbose_name="最近更新时间", auto_now=True)  # 修改数据自动设置修改当时时间


# 为方便数据添加,采用独立单表保存而不用元组choices
# 以后在自己开发设计项目或者进入公司设计表时可以参考
class IssueModule(models.Model):
    """问题所属模块表"""

    class Meta:
        verbose_name = '问题模块'  # 设置admin页面右边标题显示
        verbose_name_plural = '问题模块'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.title)

    title = models.CharField(verbose_name="模块名称", max_length=32)
    project = models.ForeignKey(verbose_name="所属项目", to=Project, on_delete=models.CASCADE)


class IssueType(models.Model):
    """问题所属类型表"""

    class Meta:
        verbose_name = '问题类型'  # 设置admin页面右边标题显示
        verbose_name_plural = '问题类型'  # 设置admin页面左边导航显示

        # 设置后台显示信息

    def __str__(self):
        return str(self.title)

    INIT_ISSUE_TYPE = ["任务", "功能", "Bug"]
    title = models.CharField(verbose_name="类型名称", max_length=32)
    project = models.ForeignKey(verbose_name="所属项目", to=Project, on_delete=models.CASCADE)
