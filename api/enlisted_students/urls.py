from django.urls import (path)
from enlisted_students.views import EnlistedStudentsViewSet

app_name = 'Enlisted Students'

enlisted_list = EnlistedStudentsViewSet.as_view({
    'get': 'list',
})

enlisted_detail = EnlistedStudentsViewSet.as_view({
    'delete': 'destroy'
})

urlpatterns = [
    path('', enlisted_list, name='enlisted-list'),
    path('<str:pk>/', enlisted_detail, name='enlisted-detail'),
]
