from django.http import Http404, JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import (viewsets, permissions, status)
from rest_framework.exceptions import ValidationError
from core.models import StudentsCourse, Course
from enlisted_students.serializers import EnlistedStudentsSerializer


class EnlistedStudentsViewSet(viewsets.ModelViewSet):
    queryset = StudentsCourse.objects.all()
    serializer_class = EnlistedStudentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    keycloak_scopes = {
        'GET': 'Class:view',
        'DELETE': 'Class:delete',
    }

    @extend_schema(
        parameters=[
            OpenApiParameter('course_id', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        course_id = request.query_params.get('course_id')

        if 'course_id' not in self.request.query_params:
            raise ValidationError('Missing required parameters course_id')

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Http404
        except ValidationError:
            return JsonResponse({"detail": "Incorrect course ID."},
                                status=status.HTTP_400_BAD_REQUEST)

        self.queryset = queryset.filter(course=course)

        return super().list(request, *args, **kwargs)
