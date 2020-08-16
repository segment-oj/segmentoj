# Serializers

from rest_framework import serializers
from account.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 0
        fields = [
            "id",
            "username",
            "lang",
            "solved",
            "submit_time",
            "email",
            "is_staff",
            "is_superuser",
            "date_joined",
            "is_active",
            "last_login",
            "email_verified",
            "list_column"
        ]
        read_only_fields = ["id", "solved", "submit_time", "date_joined", "last_login", "email", "email_verified"]

class AccountIntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 0
        fields = [
            "id",
            "introduction"
        ]
        read_only_fields = ["id"]