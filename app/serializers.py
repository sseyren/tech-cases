from rest_framework import serializers

from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        exclude = ['likes']


class FollowSerializer(serializers.Serializer):
    follow = serializers.BooleanField(required=False)
