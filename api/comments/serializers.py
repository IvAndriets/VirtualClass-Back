from rest_framework import serializers
from core.models import Comments


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')
    lecture = serializers.CharField(source='lecture_id')
    course = serializers.ReadOnlyField(source='lecture.course.id')

    class Meta:
        model = Comments
        lookup_field = 'lecture_id'
        fields = [
            'id',
            'comment',
            'lecture',
            'course',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'course', 'owner', 'created_at', 'updated_at', 'updated_by']
