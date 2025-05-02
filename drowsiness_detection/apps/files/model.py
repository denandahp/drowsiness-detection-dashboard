from django.db import models
from model_utils import Choices

from drowsiness_detection.apps.users.model import User
from drowsiness_detection.apps.cameras.model import Camera
from drowsiness_detection.core.utils import FilenameForPathGenerator


class RecordingFile(models.Model):
    TYPE = Choices(
        (1, "file", "File"),
        (2, "livestreaming", "Live Streaming"),
        (3, "googledrive", "Google Drive")
    )
    MIMETYPE = Choices(
        (1, "video", "Video"),
        (2, "image", "Image"),
        (3, "zip", "ZIP")
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to=FilenameForPathGenerator('recording_file'), blank=True, null=True) # Pake validator bolehnya mp4, webm
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_recording_files', on_delete=models.CASCADE, db_index=True)
    modified_by = models.ForeignKey(User, related_name='modified_recording_Files', on_delete=models.CASCADE, db_index=True)
    search_keyword = models.CharField(max_length=100, blank=True, null=True, db_index=True) # atau pake arrayField atau any suggestion pls
    video_meta_data = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    google_drive_id = models.CharField(max_length=255, blank=True, null=True)
    type = models.PositiveIntegerField(choices=TYPE, default=TYPE.file)
    mimetype = models.PositiveIntegerField(choices=MIMETYPE, blank=True, null=True)
    is_from_gdrive = models.BooleanField(default=False)
    camera = models.ForeignKey(Camera, related_name='camera_recording_file', on_delete=models.CASCADE, db_index=True, blank=True, null=True)
    is_display = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class ImagesFile(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to=FilenameForPathGenerator('recording_file'), blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_image', on_delete=models.CASCADE, db_index=True)
    modified_by = models.ForeignKey(User, related_name='modified_image', on_delete=models.CASCADE, db_index=True)
    camera = models.ForeignKey(Camera, related_name='camera_image_file', on_delete=models.CASCADE, db_index=True, blank=True, null=True)