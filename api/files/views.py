import mimetypes
import os
import uuid

from django.http import FileResponse, JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import FileInfo
from files.serializers import FileSerializer
from v_class_api.settings import FILE_STORAGE


class FileUploadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        operation_id='upload_file',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {
                        'type': 'string',
                        'format': 'binary'
                    }
                }
            }
        },
    )
    def post(self, request, **kwargs):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        try:
            file_obj = request.data['file']
            file_name = file_obj.name
            file_id = uuid.uuid4()

            serializer = FileSerializer(data={'file_id': file_id, 'file_name': file_name})
            serializer.is_valid()
            serializer.save(owner=request.user, file_id=file_id, file_name=file_name)

            destination = open(FILE_STORAGE + str(file_id), 'wb+')
            for chunk in file_obj.chunks():
                destination.write(chunk)
            destination.close()
        except Exception as exc:
            return JsonResponse({'detail': 'Something wne wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FileDownloadView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def get(self, request, file_id=None):
        file_object = get_object_or_404(FileInfo, id=file_id)

        file_path = FILE_STORAGE + str(file_object.file_id)
        file_name = file_object.file_name

        try:
            file = open(file_path, 'rb')
        except FileNotFoundError:
            return JsonResponse({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        mimetype, _ = mimetypes.guess_type(file_name)
        response = FileResponse(file, content_type=mimetype)
        response['Content-Length'] = os.path.getsize(file_path)
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response
