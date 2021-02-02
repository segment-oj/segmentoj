from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import StatusView
from account.models import Account

import status.JudgeStatus as js
