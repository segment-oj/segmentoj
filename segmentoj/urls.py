"""segmentoj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings

from account.views import UserView
from status.views import StatusView, StatusListCountView, StatusListView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.welcome),
    # api
    path("api/user", UserView.as_view()),
    path("api/problem/", include("problem.urls")),
    path("api/status", StatusView.as_view()),
    path("api/status/list", StatusListView.as_view()),
    path("api/status/list/count", StatusListCountView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
