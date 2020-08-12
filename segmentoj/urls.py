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

import problem.views
from account.views import AccountView, AccountSessionView, AccountUsernameAccessibilityView, AccountAvatarView, AccountPasswordView
from status.views import StatusView, StatusListCountView, StatusListView
from judger.views import JudgerStatusView, JudgerStatusDetailView
from captcha.views import getcaptcha

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.welcome),
    # api
    # Account
    path("api/account", AccountView.as_view()),
    path("api/account/<int:uid>", AccountView.as_view()),
    path("api/account/session", AccountSessionView.as_view()),
    path("api/account/username/accessibility/<str:username>", AccountUsernameAccessibilityView.as_view()),
    path("api/account/password", AccountPasswordView.as_view()),
    # Avatar
    path("api/account/avatar/<int:uid>", AccountAvatarView.as_view()),
    # Problem
    path("api/problem", problem.views.ProblemView.as_view()),
    path("api/problem/<int:pid>", problem.views.ProblemView.as_view()),
    path("api/problem/tag", problem.views.TagView.as_view()),
    path("api/problem/tag/<int:tid>", problem.views.TagView.as_view()),
    path("api/problem/list", problem.views.ProblemListView.as_view()),
    path("api/problem/list/count", problem.views.ProblemListCountView.as_view()),
    # Status
    path("api/status", StatusView.as_view()),
    path("api/status/<int:sid>", StatusView.as_view()),
    path("api/status/list", StatusListView.as_view()),
    path("api/status/list/count", StatusListCountView.as_view()),
    # Judger
    path("api/judger/status", JudgerStatusView.as_view()),
    path("api/judger/status/<int:sid>", JudgerStatusView.as_view()),
    path("api/judger/status/detail", JudgerStatusDetailView.as_view()),
    path("api/judger/status/detail/<int:sid>", JudgerStatusDetailView.as_view()),
    path("api/judger/status/detail/<int:sid>/<int:cid>", JudgerStatusDetailView.as_view()),
    # Captcha
    path("api/captcha/<int:key>", getcaptcha),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
