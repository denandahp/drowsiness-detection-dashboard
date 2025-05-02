import os
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from drowsiness_detection.apps.users.model import Role
from drowsiness_detection.apps.cameras.model import Camera
from drowsiness_detection.core.decorators import has_permission
from drowsiness_detection.core.utils import PaginatorPage
from drowsiness_detection.dashboards.cameras.forms import CreateCamerasForm

# ----------- Camera --------------
@has_permission(Role.LEVEL.admin)
def index(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    search = request.GET.get('q')
    filters = { 'q': search}

    cameras = Camera.objects.filter(created_by=request.user)
    if search:
      cameras = cameras.filter(
          Q(name__icontains=search) | 
          Q(ip_camera__icontains=search)
      ).order_by('id')


    paginator = PaginatorPage(queryset=cameras,
                              page_number=int(page),
                              limit=limit,
                              params=request.GET,
                              url='dashboards:files:index')
    context = {
        'title': 'Camera',
        'objects': paginator.objects,
        'paginator': paginator,
        'filters': filters,
        'active_tab': 'cameras',
    }
    return render(request, 'dashboards/cameras/index.html', context)

@has_permission(Role.LEVEL.admin)
def create_cameras(request):
    form = CreateCamerasForm(data=request.POST or None,
                             user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            messages.success(request, f'Create data camera {files} success')
            return redirect(reverse('dashboards:cameras:index'))

    context = {
        'form': form,
        'title': 'Create Cameras',
        'active_tab': 'cameras',
        'process': 'Create'
    }
    return render(request, 'dashboards/create.html', context)

@has_permission(Role.LEVEL.admin)
def update_cameras(request, id: int):
    recordingFile = Camera.objects.filter(id=id).first()
    form = CreateCamerasForm(data=request.POST or None,
                             instance=recordingFile,
                             user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            messages.success(request, f'Update data camera {files} success')
            return redirect(reverse('dashboards:cameras:index'))

    context = {
        'form': form,
        'title': 'Update Camera',
        'active_tab': 'cameras',
        'process': 'Update'
    }
    return render(request, 'dashboards/create.html', context)

@has_permission(Role.LEVEL.admin)
def detail_cameras(request, id: int):
    recordingFile = Camera.objects.filter(id=id).first()
    context = {
        'title': 'Cameras',
        'data': recordingFile,
        'active_tab': 'cameras',
    }
    return render(request, 'dashboards/files/detail.html', context)

@has_permission(Role.LEVEL.admin)
def delete_cameras(request, id: int):
    recordingFile = Camera.objects.filter(id=id).first()
    recordingFile.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)
