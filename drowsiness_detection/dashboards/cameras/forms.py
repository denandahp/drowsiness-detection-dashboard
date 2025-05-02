from django import forms

from drowsiness_detection.apps.cameras.model import Camera
from drowsiness_detection.apps.users.model import User


class CreateCamerasForm(forms.ModelForm):
    class Meta:
        model = Camera
        fields = ['name', 'description', 'ip_camera', 'modified_by','created_by']

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        self.fields['modified_by'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['modified_by'].initial = user
        if not self.is_update:
          self.fields['created_by'].initial = user