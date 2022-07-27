# -*- coding:utf-8 -*-
from django.urls import path, include
from web.views import user, home, project
from web.views import manage, wiki, file, setting, issue

urlpatterns = [
    # 注册登录功能
    path('home/index/', home.home_index, name='home_index'),  # 主页展示
    path('user/register/', user.user_register, name='user_register'),  # 用户注册
    path('user/login/', user.user_login, name='user_login'),  # 密码登录
    path('sms/login/', user.sms_login, name='sms_login'),  # 短信登录
    path('user/imgcode/', user.user_imgcode, name='user_imgcode'),  # 图片验证码
    path('get/sms/', user.get_sms, name='get_sms'),  # 短信验证码
    path('user/logout/', user.user_logout, name='user_logout'),  # 注销登录
    path('user/setting/', user.user_setting, name='user_setting'),  # 注销登录
    # 项目列表功能
    path('project/list/', project.project_list, name='project_list'),  # 项目列表
    # 项目星标设置参数传入
    # web/project/star/my/1/
    # web/project/star/join/1/
    path('project/star/<slug:project_type>/<int:project_id>/<slug:tf>/', project.project_star, name='project_star'),  # 项目星标
    # 项目管理页面
    # 进入项目之后路由分发
    # path('manage/<int:project_id>/dashboard', manage.manage_dashboard, name='manage_dashboard'),
    # path('manage/<int:project_id>/issues', manage.manage_issues, name='manage_issues'),
    # path('manage/<int:project_id>/statistics', manage.manage_statistics, name='manage_statistics'),
    # path('manage/<int:project_id>/file', manage.manage_file, name='manage_file'),
    # path('manage/<int:project_id>/wiki', manage.manage_wiki, name='manage_wiki'),
    # path('manage/<int:project_id>/setting', manage.manage_setting, name='manage_setting')

    path('manage/<int:project_id>/', include([
        # ##################### 项目概览 #######################################
        path('dashboard/', manage.manage_dashboard, name='manage_dashboard'),
        # ##################### 问题追踪 #######################################
        path('issue/', issue.manage_issue, name='manage_issue'),
        path('issue/add/', issue.issue_add, name='issue_add'),
        # ##################### 项目统计 #######################################
        path('statistics/', manage.manage_statistics, name='manage_statistics'),
        # ##################### 项目文件 #######################################
        path('file/', file.manage_file, name='manage_file'),
        path('file/edit/', file.file_edit, name='file_edit'),
        path('file/edit_getdata/', file.file_edit_getdata, name='file_edit_getdata'),
        path('file/delete/', file.file_delete, name='file_delete'),
        path('file/post/', file.file_post, name='file_post'),
        path('file/cos/', file.file_cos, name='file_cos'),
        path('file/download/<int:fid>/', file.file_download, name='file_download'),
        # ##################### wiki文档 #######################################
        path('wiki/', wiki.manage_wiki, name='manage_wiki'),
        path('wiki/add/', wiki.wiki_add, name='wiki_add'),
        path('wiki/upload/', wiki.wiki_upload, name='wiki_upload'),  # 项目中的文档图片按照项目级存储，一个项目对应一个对象存储桶
        path('wiki/edit/<int:wiki_id>/', wiki.wiki_edit, name='wiki_edit'),
        path('wiki/delete/<int:wiki_id>/', wiki.wiki_delete, name='wiki_delete'),
        path('wiki/catalog/', wiki.wiki_catalog, name='wiki_catalog'),
        # ##################### 项目设置 #######################################
        path('setting/all/', setting.manage_setting, name='manage_setting'),
        path('setting/edit/', setting.setting_edit, name='setting_edit'),
        path('setting/add/', setting.setting_add, name='setting_add'),
        path('setting/delete/', setting.setting_delete, name='setting_delete'),
        path('setting/delete_sure/', setting.setting_delete_sure, name='setting_delete_sure'),
    ], namespace=None), None)
]
