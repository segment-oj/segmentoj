# Serializers

from rest_framework import serializers

from status.models import Status, StatusDetail


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = ["code", "lang", "problem", "id"]
        read_only_fields = ["id"]

class StatusEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = ["state", "score", "time", "memory", "id"]
        read_only_fields = ["id"]

class StatusDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusDetail
        depth = 0
        fields = "__all__"
        read_only_fields = ["id"]