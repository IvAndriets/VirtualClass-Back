from rest_framework import (viewsets, permissions)
from core.models import Course
from course.serializers import CoursesSerializer, CoursesSerializerDetail


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
