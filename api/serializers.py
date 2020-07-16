# Serializers

from rest_framework import serializers

from problem.models import Problem, Tag
from segmentoj import tools

class ProblemSerializer(serializers.ModelSerializer):

    def get_problem(self):
        # render markdown

        obj = self.data

        content = obj.get('description')
        content = tools.markdown2html(
            content,
            obj.get('allow_htlm')
        )

        # filter needed values
        return {"id": obj.get('show_id'),
                "title": obj.get('title'), 
                "description": content,
                "tags": obj.get('tags'),
                "enabled": obj.get('enabled'),
                "date_added": obj.get('date_added')}

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
        fields = ['pid', 'title', 'enabled']
        depth = 0
        read_only_fields = ['id', 'date_added']