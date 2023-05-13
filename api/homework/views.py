import uuid

from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers, viewsets, mixins
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter
from rest_framework import (permissions, status)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.models import Lecture, Homeworks
from files.serializers import FileSerializer
from homework.serializers import HomeworksSerializer, RateWorkSerializer
from v_class_api.settings import FILE_STORAGE


class HomeworkCreateViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    queryset = Homeworks.objects.all()
    serializer_class = HomeworksSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

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

    @extend_schema(
        parameters=[
            OpenApiParameter('lecture_id', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True),
        ],
    )
    def list(self, request, *args, **kwargs):
        if 'lecture_id' not in self.request.query_params:
            raise ValidationError('Missing required parameters lecture_id')

        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=inline_serializer(
            name='InlineFormSerializerTest',
            fields={
                'file': serializers.FileField(),
                'lecture_id': serializers.UUIDField(),
                'description': serializers.CharField(),
            },
        ),
    )
    def create(self, request, *args, **kwargs):
        if 'file' not in request.data:
            raise ValidationError('Missing file')

        if 'lecture_id' not in request.data:
            raise ValidationError('Missing required field lecture_id')

        try:
            file_obj = request.data['file']
            lecture_id = request.data['lecture_id']
            description = request.data['description']
            file_name = file_obj.name
            file_id = uuid.uuid4()

            serializer = FileSerializer(data={'file_id': file_id, 'file_name': file_name, 'description': description},
                                        context={'request': request})
            serializer.is_valid()
            file = serializer.save(owner=request.user, file_id=file_id, file_name=file_name, description=description)

            destination = open(FILE_STORAGE + str(file_id), 'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()
        except Exception as exc:
            return JsonResponse({'detail': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        lecture = Lecture.objects.get(id=lecture_id)
        homework = Homeworks.objects.create(lecture=lecture, file=file, owner=self.request.user)
        homework.save()

        return Response(HomeworksSerializer(homework, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_name='rate-lab', parser_classes=[JSONParser],
            serializer_class=RateWorkSerializer)
    def rate_lab(self, request, pk=None):
        homework = get_object_or_404(Homeworks, id=pk)
        rate_serializer = RateWorkSerializer(data=request.data)
        rate_serializer.is_valid()

        homework.mark = rate_serializer.validated_data.get('mark')
        homework.teacher_comment = rate_serializer.validated_data.get('teacher_comment')
        homework.save()

        # serializer = HomeworksSerializer(homework, context={'request': request})
        # serializer.is_valid()

        # serializer.save()

        return Response(HomeworksSerializer(homework, context={'request': request}).data, status.HTTP_200_OK)
