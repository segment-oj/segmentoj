# Serializers

from django.db import models
from django.db.models import fields
from rest_framework import serializers

from status.models import Status
from problem.models import Problem

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = [
            'id'
            'code',
            'lang',
            'lang_info',
            'problem',
            'add_time',
        ]

class StatusEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = [
            'id',
            'state',
            'score',
            'time',
            'memory',
            'detail',
            'additional_info',
            'judge_by',
        ]
        read_only_fields = ['id']

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        depth = 0
        fields = [
            'pid',
            'title',
            'time_limit',
            'memory_limit',
            'testdata_url',
        ]

