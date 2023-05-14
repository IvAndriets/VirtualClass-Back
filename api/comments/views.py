from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from comments.serializers import CommentsSerializer
from core.models import Comments
from rest_framework import (permissions, mixins)


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

        self.queryset = queryset.filter(owner=self.request.user.id, lecture_id=lecture_id)

        return super().list(request, *args, **kwargs)
