from django import forms
from django.db import transaction

from django.core.validators import FileExtensionValidator

from drowsiness_detection.apps.cameras.model import Camera
from drowsiness_detection.apps.files.model import RecordingFile
from drowsiness_detection.apps.users.model import User



class CreateRecordingFile(forms.ModelForm):
    class Meta:
        model = RecordingFile
        fields = ['type', 'camera', 'name', 'description', 'search_keyword', 
                  'video_meta_data', 'file', 'created_by', 'modified_by',
                  'url', 'google_drive_id', 'mimetype']

    file = forms.FileField(
        label='File Video', required=False,
        help_text='File harus dalam format MP4 atau WebM.',
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'webm'])
        ])
    TYPE_CHOICE = (
          (1, "File"),
          (3, "Google Drive")
    )
    type = forms.ChoiceField(choices=TYPE_CHOICE)

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        self.fields['video_meta_data'].widget = forms.HiddenInput()
        self.fields['modified_by'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['camera'].queryset = Camera.objects.filter(created_by=user)
        self.fields['google_drive_id'].required = False
        self.fields['google_drive_id'].help_text = "Wajib mengisi 'Google Drive Id'"
        self.fields['modified_by'].initial = user
        if not self.is_update:
          self.fields['created_by'].initial = user

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and 'drive.google.com' in url:
            url = url.replace("view", "preview")
        return url

    def clean_google_drive_id(self):
        types = self.cleaned_data.get('type')
        gdrive_id = self.cleaned_data.get('google_drive_id')
        if types == RecordingFile.TYPE.googledrive and not gdrive_id:
            raise forms.ValidationError(
                'Wajib mengisi "gdrive id" jika centang dari google drive',
                code="invalid_isFromZGdrive")
        return gdrive_id


class CreateLiveStreaming(forms.ModelForm):
    class Meta:
        model = RecordingFile
        fields = ['type', 'camera', 'name', 'description', 'search_keyword', 
                  'created_by', 'modified_by', 'url', 'is_display']

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
        self.fields['camera'].queryset = Camera.objects.filter(created_by=user)
        self.fields['modified_by'].widget = forms.HiddenInput()
        self.fields['created_by'].widget = forms.HiddenInput()
        self.fields['is_display'].widget.attrs['form_switch'] = True
        self.fields['modified_by'].initial = user
        self.fields['type'].initial = RecordingFile.TYPE.livestreaming
        self.fields['type'].widget = forms.HiddenInput()
        self.fields['is_display'].help_text = "Untuk memunculkan dihalaman monitoring"
        if not self.is_update:
          self.fields['created_by'].initial = user
        else:
          self.fields['camera'].initial = self.instance.camera