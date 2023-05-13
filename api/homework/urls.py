from homework.views import HomeworkCreateViewSet
from django.urls import (path, include)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', HomeworkCreateViewSet)

app_name = 'Homework'

urlpatterns = [
    path('', include(router.urls)),
]
