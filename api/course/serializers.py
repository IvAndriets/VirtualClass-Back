from rest_framework import serializers
from core.models import Course


class CoursesSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'active',
            'description',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'active', 'created_at', 'updated_at', 'updated_by']
