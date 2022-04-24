from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .rest import *

app_name = 'hfntr'

urlpatterns = [
    path('upload/', upload_file),
    path('status/<int:file_id>/', file_status),
    path('download/<int:file_id>/', download_file_url),
    path('file/', HyphenatedFileList.as_view()),
    path('file/<int:pk>/', HyphenatedFileDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
