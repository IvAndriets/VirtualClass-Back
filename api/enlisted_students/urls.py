from django.urls import (path)
from enlisted_students.views import EnlistedStudentsViewSet
from enlisted_students.views_join import JoinClassViewSet

app_name = 'Enlisted Students'

enlisted_list = EnlistedStudentsViewSet.as_view({
    'get': 'list',
})

enlisted_detail = EnlistedStudentsViewSet.as_view({
    'delete': 'destroy'
})

join_course = JoinClassViewSet.as_view({
    'post': 'join_course'
})

urlpatterns = [
    path('join-course/', join_course, name='join-course'),
    path('', enlisted_list, name='enlisted-list'),
    path('<str:pk>/', enlisted_detail, name='enlisted-detail'),
]
