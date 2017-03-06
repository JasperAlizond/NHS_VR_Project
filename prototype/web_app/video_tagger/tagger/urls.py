"""video_tagger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.http import Http404
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
        url(r"^login/", auth_views.login),

        url(r"^project/", project_list),
        url(r"^project/new/", project_create),
        url(r"^project/([0-9]+)/", project_detail),
        url(r"^project/([0-9]+)/delete/", project_delete),
        url(r"^project/([0-9]+)/export", project_export),
        
        url(r"^video/", video_list),
        url(r"^video/new/", video_create),
        url(r"^video/([0-9]+)/", video_editor),
        url(r"^video/([0-9]+)/delete/", video_delete),


]
