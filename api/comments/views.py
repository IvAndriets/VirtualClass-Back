import os

from django.db.models import Prefetch
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from comments.serializers import CommentsSerializer
from core.models import Comments, Lecture, Course
from rest_framework import (permissions, mixins, status)


class CommentsViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = {
        'comment': [
            'icontains',
            'exact',
        ]}

    search_fields = ['$comment']
    ordering_fields = '__all__'

    keycloak_scopes = {
        'GET': 'Class:view',
        'POST': 'Class:view',
        'DELETE': 'Class:delete'
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter('lecture_id', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True),
        ],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        lecture_id = self.request.query_params.get('lecture_id')

        if 'lecture_id' not in self.request.query_params:
            raise ValidationError('Missing required parameters lecture_id')

        if self.is_student():
            crs = Course.objects.prefetch_related('students').filter(students__student=self.request.user)
            lectures = Lecture.objects.prefetch_related(Prefetch('course', queryset=crs))
            query_set = Comments.objects.prefetch_related(Prefetch('lecture', queryset=lectures))\
                .filter(lecture_id=lecture_id)
        else:
            query_set = queryset.filter(lecture_id=lecture_id)

        self.queryset = query_set

        return super().list(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comments, id=pk)
        lecture = get_object_or_404(Lecture, id=comment.lecture_id)

        if lecture.owner == request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

    def is_student(self):
        roles = self.request.auth.payload['resource_access'][os.environ.get('OIDC_RP_CLIENT_ID')]['roles']
        return 'Student' in roles
