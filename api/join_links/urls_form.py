from django.urls import (path)
from join_links.views import JoinLink

app_name = 'join_course'

urlpatterns = [
    path('<str:pk>/', JoinLink.as_view(), name='join-course'),
]
