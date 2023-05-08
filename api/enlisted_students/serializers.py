from rest_framework import serializers
from core.models import StudentsCourse


class EnlistedStudentsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')

    class Meta:
        model = StudentsCourse
        fields = [
            'id',
            'course',
            'student',
            'join_link',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'updated_by']


class JoinClassSerializer(serializers.ModelSerializer):
    access_code = serializers.CharField(max_length=255)

    class Meta:
        model = StudentsCourse
        fields = [
            'access_code',
        ]
