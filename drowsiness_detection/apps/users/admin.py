from django.contrib import admin

from drowsiness_detection.apps.users.model import User, Role

admin.site.register(User)
admin.site.register(Role)