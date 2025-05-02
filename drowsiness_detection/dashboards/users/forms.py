from typing import Any
from django import forms

from drowsiness_detection.apps.users.model import User
from drowsiness_detection.core.services.google import googledrive_service
from drowsiness_detection.core.utils import normalize_phone


class UpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = normalize_phone(phone_number)
        return phone_number

class UpdateConnection(forms.ModelForm):
    class Meta:
        model = User
        fields = ['isAuthGDrive']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
    
    def clean(self) -> dict[str, Any]:
        data = super().clean()
        isAuthGDrive = data.get('isAuthGDrive')
        googleService = googledrive_service(self.user) if isAuthGDrive else None
        data['isAuthGDrive'] = True if googleService else False