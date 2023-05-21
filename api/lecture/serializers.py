from rest_framework import serializers
from core.models import Lecture, FileInfo
from files.serializers import FileSerializer


class LectureSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')
    course = serializers.ReadOnlyField(source='course.id')
    # files = serializers.HyperlinkedIdentityField(
    #     view_name='files:download-file',
    #     lookup_field='file_id',
    #     many=True,
    #     read_only=True,
    # )
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Lecture
        lookup_field = 'course_id'
        fields = [
            'id',
            'course',
            'name',
            'files',
            'active',
            'description',
            'type',
            'max_grade',
            'due_date',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'course', 'active', 'created_at', 'updated_at', 'updated_by']
