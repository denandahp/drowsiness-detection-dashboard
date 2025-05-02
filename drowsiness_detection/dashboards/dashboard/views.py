from datetime import datetime
from django.db.models import Count, F, Func, Value, CharField
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek, ExtractWeekDay
from django.conf import settings
from django.shortcuts import render

from drowsiness_detection.apps.users.model import Role
from drowsiness_detection.apps.files.model import RecordingFile
from drowsiness_detection.core.decorators import has_permission

@has_permission(Role.LEVEL.admin)
def monitor(request):
    recordingFiles = RecordingFile.objects.filter(
        created_by=request.user,
        type=RecordingFile.TYPE.livestreaming,
        is_display=True
    ).order_by('-id')[:4]

    allRecordingFiles = RecordingFile.objects.filter(created_by=request.user).order_by('-id')[:10]

    context = {
        'title': 'Monitor Live Streaming',
        'objects': allRecordingFiles,
        'datas': recordingFiles,
        'active_tab': 'monitor',
        'refresh_page': settings.REFRESH_MONITOR_PAGE

    }
    return render(request, 'dashboards/dashboard/monitor.html', context)

@has_permission(Role.LEVEL.admin)
def dashboard(request):
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')
    typeList = [x for x, y in RecordingFile.TYPE if x != RecordingFile.TYPE.livestreaming]

    recordingFiles = RecordingFile.objects.annotate(
          createdDate=Func(
            F('created'),
            Value('yyyy-MM-dd hh:mm'),
            function='to_char',
            output_field=CharField()
          )
        ).filter(
            created_by=request.user,
            created__range=(startDate, endDate),
            type__in=typeList
        ).values(
            'createdDate'
        ).annotate(
            count=Count('id')
        ).order_by('createdDate')

    statistikData = {
        'xAxis': [x.get('count') for x in recordingFiles],
        'yAxis': [x.get('createdDate') for x in recordingFiles]
    }

    context = {
        'datas': recordingFiles,
        'statistikData': statistikData,
        'active_tab': 'dashboard',
        'refresh_page': settings.REFRESH_MONITOR_PAGE

    }
    return render(request, 'dashboards/dashboard/detail.html', context)