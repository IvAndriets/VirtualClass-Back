from rest_framework import serializers
from core.models import CourseLinks


class JoinLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )


class CourseLinkSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')
    course_id = serializers.CharField()

    class Meta:
        model = CourseLinks
        fields = [
            'id',
            'use_access_code',
            'access_code',
            'course_id',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'updated_by']
