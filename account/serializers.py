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
            "introduction",
            "lang",
            "solved",
            "submit_time",
            "email",
            "is_staff",
            "is_superuser",
            "date_joined",
            "is_active",
            "last_login",
            "email_verified"
        ]
        read_only_fields = ["id", "solved", "submit_time", "date_joined", "last_login", "email", "email_verified"]

