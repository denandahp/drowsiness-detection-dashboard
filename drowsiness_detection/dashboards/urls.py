from django.urls import path, include
from drowsiness_detection.dashboards.dashboard.views import dashboard, monitor

app_name = 'dashboards'

urlpatterns = [
    path('', dashboard, name="index"),
    path('files/', include(
        'drowsiness_detection.dashboards.files.urls', namespace='files')),
    path('user/', include(
        'drowsiness_detection.dashboards.users.urls', namespace='users')),
    path('cameras/', include(
        'drowsiness_detection.dashboards.cameras.urls', namespace='cameras')),
    path('monitor', monitor, name="monitor_dashboard")
]