from rest_framework import serializers
from core.models import Homeworks
from files.serializers import FileSerializer


class HomeworksSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    updated_by = serializers.ReadOnlyField(source='updated_by.email')
    lecture = serializers.CharField(source='lecture_id')
    file = FileSerializer()

    class Meta:
        model = Homeworks
        lookup_field = 'lecture_id'
        fields = [
            'id',
            'lecture',
            'mark',
            'file',
            'teacher_comment',
            'owner',
            'created_at',
            'updated_at',
            'updated_by',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'updated_by']


class RateWorkSerializer(serializers.Serializer):
    mark = serializers.IntegerField()
    teacher_comment = serializers.CharField(max_length=255)

