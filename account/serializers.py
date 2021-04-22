# Serializers

from rest_framework import serializers
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        depth = 0
        fields = [
            'id',
            'username',
            'lang',
            'solved',
            'submit_time',
            'email',
            'is_staff',
            'is_superuser',
            'is_active',
            'is_judger',
            'date_joined',
            'last_login',
            'email_verified',
            'avatar_url',
        ]
        read_only_fields = [
            'id',
            'solved',
            'submit_time',
            'date_joined',
            'last_login',
            'email',
            'email_verified'
        ]


class AccountIntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        depth = 0
        fields = [
            'id',
            'introduction'
        ]
        read_only_fields = ['id']


class AccountExtraDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        depth = 0
        fields = [
            'id',
            'extra_data'
        ]
        read_only_fields = ['id']
