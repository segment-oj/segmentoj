# Serializers

from rest_framework import serializers

from problem.models import Problem, Tag
from segmentoj import tools

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "pid", 
            "date_added", 
            "title", 
            "description",
            "allow_html", 
            "tags", 
            "enabled", 
            "memory_limit", 
            "time_limit",
        ]

        depth = 0
        read_only_fields = ["id", "date_added"]

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