from django.urls import path

from drowsiness_detection.dashboards.files.views import (
  create_recording_files, index, update_recording_files,
  detail_recording_files, sync_file_from_googledrive,
  index_livestreaming, create_livestreaming, delete_recording_files
)

app_name = 'files'

urlpatterns = [
    # Recording File
    path('', index, name="index"),
    path('add', create_recording_files, name="add_files"),
    path('edit/<int:id>', update_recording_files, name="edit_files"),
    path('detail/<int:id>', detail_recording_files, name="detail_files"),
    path('delete/<int:id>', delete_recording_files, name="delete_files"),

    # Live Streaming
    path('liveStreaming', index_livestreaming, name="index_livestreaming"),
    path('liveStreaming/add', create_livestreaming, name="add_livestreaming"),
    path('liveStreaming/edit/<int:id>', update_recording_files, name="edit_livestreaming"),

    # Google Drive
    path('syncGoogleDrive', sync_file_from_googledrive, name="sync_file_googledrive"),
]
