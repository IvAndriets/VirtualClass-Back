from rest_framework import (viewsets, permissions)
from core.models import Course
from course.serializers import CoursesSerializer


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
