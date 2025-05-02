from django import forms
from django.contrib.auth.forms import AuthenticationForm

from drowsiness_detection.apps.users.model import User, Role
from drowsiness_detection.core.utils import normalize_phone

class LoginAuthForm(AuthenticationForm):
    username = forms.EmailField(label='Email User')

    def __init__(self, *args, **kwargs):
        super(LoginAuthForm, self).__init__(*args, **kwargs)


class UserRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'role']
    
    role = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_update = self.instance.id
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email=email).first()
        if email_exist:
            raise forms.ValidationError('Email telah di daftarkan.',
                                        code='invalid_email')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        phone_number = normalize_phone(phone_number)
        return phone_number

    def save(self):
        data = super().clean()
        roleAdmin = Role.objects.filter(id=1).first()
        extra_fields = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'phone_number': data.get('phone_number'),
            'role': roleAdmin
            
        }
        User.objects.create_user(email=data.get('email') , password=data.get('password'), **extra_fields)
        return data
