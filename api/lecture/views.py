from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from rest_framework import (viewsets, permissions)
from core.models import Lecture, Course
from lecture.serializers import LectureSerializer
from rest_framework import status


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
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
        serializer.save(owner=self.request.user, course_id=self.request.course.id)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')

        try:
            course = Course.objects.get(**{'id': course_id})
        except Course.DoesNotExist:
            return Http404
        except ValidationError:
            return JsonResponse({"detail": "Incorrect course ID."},
                                status=status.HTTP_400_BAD_REQUEST)

        request.course = course

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user.id)
        return query_set

    def list(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')

        try:
            course = Course.objects.get(**{'id': course_id})
        except Course.DoesNotExist:
            return Http404
        except ValidationError:
            return JsonResponse({"detail": "Incorrect course ID."},
                                status=status.HTTP_400_BAD_REQUEST)

        self.queryset = Lecture.objects.filter(course_id=course.id)
        return super().list(request, *args, **kwargs)
