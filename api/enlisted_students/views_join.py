from django.http import JsonResponse
from rest_framework import (viewsets, permissions, status)
from rest_framework.response import Response
from core.models import StudentsCourse, Course, CourseLinks
from enlisted_students.serializers import JoinClassSerializer


class JoinClassViewSet(viewsets.ModelViewSet):
    serializer_class = JoinClassSerializer
    permission_classes = [permissions.IsAuthenticated]

    keycloak_scopes = {
        'POST': 'Class:view',
    }

    def join_course(self, request):
        serializer = JoinClassSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse({"detail": "Incorrect ACCESS CODE."},
                                status=status.HTTP_400_BAD_REQUEST)

        access_code = serializer.validated_data.get('access_code')

        try:
            link = CourseLinks.objects.get(access_code=access_code, active=True, use_access_code=True)
        except CourseLinks.DoesNotExist:
            return JsonResponse({"detail": "There is no such ACCESS CODE or it is no longer active :(."},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(**{'id': link.course_id, 'active': True})
        except Course.DoesNotExist:
            return JsonResponse({"detail": "There is no active COURSE with this code :(."},
                                status=status.HTTP_400_BAD_REQUEST)

        enroll_students = StudentsCourse.objects.filter(course=course, student=request.user)

        try:
            if not enroll_students:
                new_enrollment = StudentsCourse.objects.create(
                    course=course, join_link=link, student=request.user, owner=request.user)
                new_enrollment.save()
        except Exception:
            return JsonResponse({"detail": "Cannot join course."},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'ok'})
