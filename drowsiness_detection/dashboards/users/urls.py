from django.urls import path

from drowsiness_detection.dashboards.users.views import (
  edit_user, edit_connection
)

app_name = 'users'

urlpatterns = [
    # path('', index, name="index"),
    path('edit_connection/<int:id>', edit_connection, name="edit_connection"),
    path('edit/<int:id>', edit_user, name="edit_user"),
    # path('detail/<int:id>', detail_recording_files, name="detail_files")
]
