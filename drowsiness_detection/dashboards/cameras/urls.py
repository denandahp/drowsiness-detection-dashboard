from django.urls import path

from drowsiness_detection.dashboards.cameras.views import (
  create_cameras, index, update_cameras,
  detail_cameras, delete_cameras
)

app_name = 'cameras'

urlpatterns = [
    path('', index, name="index"),
    path('add', create_cameras, name="add_cameras"),
    path('edit/<int:id>', update_cameras, name="edit_cameras"),
    path('detail/<int:id>', detail_cameras, name="detail_cameras"),
    path('delete/<int:id>', delete_cameras, name="delete_cameras"),
]
