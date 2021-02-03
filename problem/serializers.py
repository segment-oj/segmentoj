# Serializers

from rest_framework import serializers

from problem.models import Problem, Tag

class ProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = [
            "pid",
            "date_added",
            "last_edit",
            "title",
            "description",
            "allow_html",
            "tags",
            "enabled",
            "memory_limit",
            "time_limit",
        ]

        depth = 0
        read_only_fields = ["id", "date_added", "last_edit"]
        extra_kwargs = {
            "description": {"write_only": True},
        }

class ProblemDescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = [
            "description",
        ]

        depth = 0

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ["id"]

class ProblemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ["id", "pid", "title", "enabled", "tags"]
        depth = 0
        read_only_fields = ["id"]