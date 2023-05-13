from rest_framework import serializers
from core.models import Course
from enlisted_students.serializers import EnlistedStudentsSerializer
from lecture.serializers import LectureSerializer


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


class CoursesSerializerDetail(CoursesSerializer):
    lectures = LectureSerializer(many=True, read_only=True)
    students = EnlistedStudentsSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'active',
            'description',
            'full_description',
            'lectures',
            'students',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'active', 'created_at', 'updated_at', 'updated_by']


class DescriptionSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=255)
