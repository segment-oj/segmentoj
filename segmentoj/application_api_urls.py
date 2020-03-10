# application api

from django.contrib import admin
from django.urls import path, include
from . import api

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('user/login', api.login_api),
    path('user/logout', api.logout_api),
    path('user/register', api.register_api),
]
