# Serializers

from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerialize(serializers.Serializer):

	class Meta:
		model = User
		fields = ("id", "username", "email", "is_staff", "is_active", )