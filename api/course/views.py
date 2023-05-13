import uuid
from rest_framework import serializers
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import (viewsets, permissions, status)
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import Course, Lecture
from course.serializers import CoursesSerializer, CoursesSerializerDetail, DescriptionSerializer
from files.serializers import FileSerializer
from v_class_api.settings import FILE_STORAGE


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CoursesSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = {
        'name': [
            'icontains',
            'exact',
        ],
        'description': [
            'icontains',
        ]}

    search_fields = ['$name', '$description']
    ordering_fields = '__all__'

    keycloak_scopes = {
        'GET': 'Class:view',
        'POST': 'Class:add',
        'PATCH': 'Class:update',
        'PUT': 'Class:update',
        'DELETE': 'Class:delete'
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user.id)
        return query_set

    def get_serializer_class(self):
        if self.action == 'list':
            return CoursesSerializer
        else:
            return CoursesSerializerDetail


class LectureFilesView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return DescriptionSerializer

    @extend_schema(
        request=inline_serializer(
            name='InlineFormSerializer',
            fields={
                'file': serializers.FileField(),
                'description': serializers.IntegerField(),
            },
        ),
    )
    def post(self, request, course_id, lecture_id, **kwargs):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        try:
            file_obj = request.data['file']
            description = request.data['description']
            file_name = file_obj.name
            file_id = uuid.uuid4()

            serializer = FileSerializer(data={'file_id': file_id, 'file_name': file_name, description: description})
            serializer.is_valid()
            file = serializer.save(owner=request.user, file_id=file_id, file_name=file_name, description=description)

            destination = open(FILE_STORAGE + str(file_id), 'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()
        except Exception as exc:
            return JsonResponse({'detail': 'Something wne wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lecture = Lecture.objects.get(id=lecture_id)
        lecture.files.add(file)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
