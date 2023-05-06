from rest_framework import serializers
from core.models import Lecture


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')
    course = serializers.ReadOnlyField(source='course.id')

    class Meta:
        model = Lecture
        lookup_field = 'course_id'
        fields = [
            'id',
            'course',
            'name',
            'active',
            'description',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'course', 'active', 'created_at', 'updated_at', 'updated_by']
