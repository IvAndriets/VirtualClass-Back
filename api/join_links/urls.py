from django.urls import (path, include)
from rest_framework.routers import DefaultRouter
from join_links.views import JoinLink, CourseLinksViewSet

router = DefaultRouter()
router.register('', CourseLinksViewSet)

app_name = 'join_course'

urlpatterns = [
    path('', include(router.urls)),
]

urlpatternsJoin = [
    path('', JoinLink.as_view()),
]
