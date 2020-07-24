# Serializers

from rest_framework import serializers

from status.models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        depth = 0
        fields = ["code", "lang", "problem", "id"]
        read_only_fields = ["id"]


