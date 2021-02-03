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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.views import (
    AccountView,
    AccountIntroductionView,
    AccountUsernameAccessibilityView,
    # AccountAvatarView,
    AccountPasswordView,
    AccountEmailView,
)
from status.views import StatusView, StatusListView
from captcha.views import get_captcha

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome),
    # api
    # Account
    path('api/account', AccountView.as_view()),
    path('api/account/<int:uid>', AccountView.as_view()),
    path('api/account/<int:uid>/introduction', AccountIntroductionView.as_view()),
    path('api/account/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/account/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/username/accessibility/<str:username>', AccountUsernameAccessibilityView.as_view()),
    path('api/account/password', AccountPasswordView.as_view()),
    path('api/account/email', AccountEmailView.as_view()),
    path('api/account/email/<str:vid>', AccountEmailView.as_view()),
    # Avatar
    # path('api/account/avatar/<int:uid>', AccountAvatarView.as_view()),
    # Problem
    path('api/problem', problem.views.ProblemView.as_view()),
    path('api/problem/<int:pid>', problem.views.ProblemView.as_view()),
    path('api/problem/<int:pid>/description', problem.views.ProblemDescriptionView.as_view()),
    path('api/problem/list', problem.views.ProblemListView.as_view()),
    path('api/problem/tag', problem.views.TagView.as_view()),
    path('api/problem/tag/<int:tid>', problem.views.TagView.as_view()),
    path('api/problem/tag/list', problem.views.TagListView.as_view()),
    # Status
    path('api/status', StatusView.as_view()),
    path('api/status/<int:sid>', StatusView.as_view()),
    path('api/status/list', StatusListView.as_view()),
    # Judger
    # Captcha
    path('api/captcha/<int:key>', get_captcha),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
