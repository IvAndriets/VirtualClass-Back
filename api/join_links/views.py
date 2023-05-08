from django.core.management.utils import get_random_secret_key
from django.http import HttpResponseNotFound
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.exceptions import ValidationError
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from core.models import CourseLinks, Course, StudentsCourse, User
from join_links.serializers import JoinLinkSerializer, CourseLinkSerializer
from rest_framework import (viewsets, permissions)


class JoinLink(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'join_links/join-class.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk=None):
        if not pk:
            return HttpResponseNotFound('Incorrect join course link.')

        try:
            link = CourseLinks.objects.get(id=pk, active=True)
        except CourseLinks.DoesNotExist:
            return HttpResponseNotFound('There is no such join link or link is no longer active :(')
        except Exception as exc:
            return HttpResponseNotFound('There is incorrect join link :(')

        try:
            course = Course.objects.get(**{'id': link.course_id, 'active': True})
        except Course.DoesNotExist:
            return HttpResponseNotFound('There is no such course :(')

        serializer = JoinLinkSerializer({'email': ''})
        return Response({'serializer': serializer, 'course': course, 'link': link})

    def post(self, request, pk=None):
        try:
            link = CourseLinks.objects.get(id=pk, active=True)
        except CourseLinks.DoesNotExist:
            return HttpResponseNotFound('There is no such join link or link is no longer active :(')

        try:
            course = Course.objects.get(**{'id': link.course_id, 'active': True})
        except Course.DoesNotExist:
            return HttpResponseNotFound('There is no such course :(')

        serializer = JoinLinkSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(template_name='join_links/failure.html')

        email = serializer.validated_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(template_name='join_links/failure.html')

        enroll_students = StudentsCourse.objects.filter(course=course, student=user)

        try:
            if not enroll_students:
                new_enrollment = StudentsCourse.objects.create(course=course, join_link=link, student=user, owner=user)
                new_enrollment.save()
        except Exception:
            return Response(template_name='join_links/failure.html')

        return Response(template_name='join_links/success.html')


class CourseLinksViewSet(viewsets.ModelViewSet):
    queryset = CourseLinks.objects.all()
    serializer_class = CourseLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = {
        'access_code': [
            'icontains',
            'exact',
        ]}

    search_fields = ['$access_code']
    ordering_fields = '__all__'

    keycloak_scopes = {
        'GET': 'Class:view',
        'POST': 'Class:add',
        'PATCH': 'Class:update',
        'PUT': 'Class:update',
        'DELETE': 'Class:delete'
    }

    def perform_create(self, serializer):
        use_access_code = serializer.validated_data.get('use_access_code')
        access_code = serializer.validated_data.get('access_code')
        access_code = access_code if access_code and use_access_code else get_random_secret_key()
        serializer.save(owner=self.request.user, access_code=access_code)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        queryset = self.queryset

        course_id = self.request.query_params.get('course_id')

        if 'course_id' not in self.request.query_params:
            raise ValidationError('Missing required parameters course_id')

        query_set = queryset.filter(owner=self.request.user.id, course_id=course_id)
        return query_set

    @extend_schema(
        parameters=[
            OpenApiParameter('course_id', OpenApiTypes.UUID, OpenApiParameter.QUERY, required=True),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
