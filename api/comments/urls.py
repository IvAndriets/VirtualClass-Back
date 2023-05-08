from django.urls import (path, include)
from rest_framework.routers import DefaultRouter
from comments.views import CommentsViewSet


router = DefaultRouter()
router.register('', CommentsViewSet)

app_name = 'Comments'

urlpatterns = [
    path('', include(router.urls)),
]
