# Serializers

from rest_framework import serializers

from problem.models import Problem, Tag
from segmentoj import tools

class ProblemSerializer(serializers.ModelSerializer):

    def get_problem(self):
        # render markdown

        obj = self.data

        content = obj.get('description')

        # filter needed values
        return {"pid": obj.get('pid'),
                "title": obj.get('title'), 
                "description": content,
                "tags": obj.get('tags'),
                "enabled": obj.get('enabled'),
                "date_added": obj.get('date_added'),
                "allow_html": obj.get('allow_html')}

    class Meta:
        model = Problem
        fields = '__all__'
        depth = 0
        read_only_fields = ['id', 'date_added']

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ['id']

class ProblemListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ['id', 'pid', 'title', 'enabled']
        depth = 0
        read_only_fields = ['id', 'date_added']