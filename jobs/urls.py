# -*- coding: utf-8 -*-
"""
# @Author : qgc
# @Time : 2022/11/15 15:46
# @File : urls.py
# Description : 文件说明
"""
from django.urls import path,re_path
from jobs import views


urlpatterns = [
    # 职位列表
    re_path(r"^joblist/", views.joblist, name='joblist'),
    re_path(r"^job/(?P<job_id>\d+)/$", views.detail, name='detail')
]