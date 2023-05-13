from django.urls import (path)
from course.views import CourseViewSet, LectureFilesView, LectureGetFileView
from lecture.views import LectureViewSet

app_name = 'Course'

course_list = CourseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

course_detail = CourseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

lecture_list = LectureViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

lecture_detail = LectureViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', course_list, name='class-list'),
    path('<str:pk>/', course_detail, name='class-detail'),
    path('<str:course_id>/lectures/', lecture_list, name='lecture-list'),
    path('<str:course_id>/lectures/<str:pk>/', lecture_detail, name='lecture-detail'),
    path('<str:course_id>/lectures/<str:lecture_id>/files/', LectureFilesView.as_view(), name='lecture-detail-files'),
    path('<str:course_id>/lectures/<str:lecture_id>/files/<str:file_id>',
         LectureGetFileView.as_view(), name='lecture-get-file'),
]
