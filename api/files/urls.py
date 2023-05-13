from django.urls import (path)
from files.views import FileUploadView, FileDownloadView

app_name = 'Files'

urlpatterns = [
    path('', FileUploadView.as_view(), name='upload-file'),
    path('<str:file_id>', FileDownloadView.as_view(), name='download-file'),
]
