from django.urls import path

from drowsiness_detection.dashboards.auth.views import (
  signup, login_dashboards, logout_dashboards, googledrive_auth
)

app_name = 'auth'

urlpatterns = [
    path('login', login_dashboards, name='login'),
    path('googledrive', googledrive_auth, name='googledrive_auth'),
    path('signup', signup, name="signup"),
    path('logout', logout_dashboards, name="logout"),
]
