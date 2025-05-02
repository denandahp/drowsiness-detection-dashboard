from django.db import models

from drowsiness_detection.apps.users.model import User


class Camera(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    ip_camera = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_camera', on_delete=models.CASCADE, db_index=True)
    modified_by = models.ForeignKey(User, related_name='modified_camera', on_delete=models.CASCADE, db_index=True)

    def __str__(self) -> str:
        return self.name