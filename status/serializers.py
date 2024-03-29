# Serializers

from rest_framework import serializers
from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = '__all__'


class StatusListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = [
            'id',
            'add_time',
            'score',
            'lang',
            'time',
            'memory',
            'owner',
            'problem',
            'state',
        ]
