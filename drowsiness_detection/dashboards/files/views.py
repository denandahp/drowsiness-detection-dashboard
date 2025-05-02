import os
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from drowsiness_detection.apps.users.model import Role
from drowsiness_detection.apps.files.model import RecordingFile
from drowsiness_detection.core.decorators import has_permission
from drowsiness_detection.core.utils import PaginatorPage
from drowsiness_detection.core.services.google import googledrive_service
from drowsiness_detection.core.services.twilio import send_whatsapp
from drowsiness_detection.dashboards.files.forms import CreateRecordingFile, CreateLiveStreaming

# ----------- Recording File --------------
@has_permission(Role.LEVEL.admin)
def index(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    search = request.GET.get('q')
    orderby = request.GET.get('orderby') if request.GET.get('orderby') else '-id'
    typeFilter = request.GET.get('type')
    filters = { 'q': search, 'orderby': orderby, 'typeFilter': typeFilter}

    typeChoice = [RecordingFile.TYPE.file, RecordingFile.TYPE.googledrive]
    recordingFiles = RecordingFile.objects.filter(created_by=request.user, type__in=typeChoice).order_by(orderby)
    if search:
      recordingFiles = recordingFiles.filter(
          Q(name__icontains=search) | 
          Q(search_keyword__icontains=search)
      ).order_by('id')

    if typeFilter: recordingFiles = recordingFiles.filter(type=RecordingFile.TYPE._identifier_map[typeFilter])

    paginator = PaginatorPage(queryset=recordingFiles,
                              page_number=int(page),
                              limit=limit,
                              params=request.GET,
                              url='dashboards:files:index')
    context = {
        'title': 'Recording File',
        'objects': paginator.objects,
        'paginator': paginator,
        'filters': filters,
        'active_tab': 'file',
        'active_sub_tab': 'recordingFile'
    }
    return render(request, 'dashboards/files/index.html', context)

@has_permission(Role.LEVEL.admin)
def create_recording_files(request):
    form = CreateRecordingFile(data=request.POST or None,
                               files=request.FILES or None,
                               user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            send_whatsapp(f'Recording files {files.name} successfully create', request.user.phone_number)
            messages.success(request, f'Create files {files} success')
            return redirect(reverse('dashboards:files:index'))

    context = {
        'form': form,
        'typeList': RecordingFile.TYPE,
        'title': 'Create Recording Files',
        'active_tab': 'file',
        'active_sub_tab': 'recordingFile',
        'process': 'Create'
    }
    return render(request, 'dashboards/files/create.html', context)

@has_permission(Role.LEVEL.admin)
def update_recording_files(request, id: int):
    recordingFile = RecordingFile.objects.filter(id=id).first()
    form = CreateRecordingFile(data=request.POST or None,
                               files=request.FILES or None,
                               instance=recordingFile,
                               user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            messages.success(request, f'Update recording file {files} success')
            return redirect(reverse('dashboards:files:index'))

    context = {
        'form': form,
        'title': 'Update Recording File',
        'active_tab': 'file',
        'active_sub_tab': 'recordingFile',
        'process': 'Update'
    }
    return render(request, 'dashboards/files/create.html', context)

@has_permission(Role.LEVEL.admin)
def detail_recording_files(request, id: int):
    recordingFile = RecordingFile.objects.filter(id=id).select_related('camera').first()
    context = {
        'title': 'Recording Files',
        'data': recordingFile,
        'active_tab': 'file',
        'active_sub_tab': 'recordingFile'
    }
    return render(request, 'dashboards/files/detail.html', context)

@has_permission(Role.LEVEL.admin)
def delete_recording_files(request, id: int):
    recordingFile = RecordingFile.objects.filter(id=id).select_related('camera').first()
    recordingFile.delete()
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer)

# ------------- Live Streaming -------------

@has_permission(Role.LEVEL.admin)
def index_livestreaming(request):
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 10)
    search = request.GET.get('q')
    orderby = request.GET.get('orderby') if request.GET.get('orderby') else '-id'
    filters = { 'q': search, 'orderby': orderby }

    files = RecordingFile.objects.filter(created_by=request.user, type=RecordingFile.TYPE.livestreaming).order_by(orderby)
    if search:
      files = files.filter(
          Q(name__icontains=search) | 
          Q(search_keyword__icontains=search)
      ).order_by('id')


    paginator = PaginatorPage(queryset=files,
                              page_number=int(page),
                              limit=limit,
                              params=request.GET,
                              url='dashboards:files:index_livestreaming')
    context = {
        'title': 'Live Streaming',
        'objects': paginator.objects,
        'paginator': paginator,
        'filters': filters,
        'active_tab': 'file',
        'active_sub_tab': 'liveStreaming'
    }
    return render(request, 'dashboards/files/index_livestreaming.html', context)

@has_permission(Role.LEVEL.admin)
def create_livestreaming(request):
    form = CreateLiveStreaming(data=request.POST or None,
                               user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            send_whatsapp(f'Live streaming {files.name} successfully create', request.user.phone_number)
            messages.success(request, f'Create files {files} success')
            return redirect(reverse('dashboards:files:index_livestreaming'))

    context = {
        'form': form,
        'typeList': RecordingFile.TYPE,
        'title': 'Create Live Streaming',
        'active_tab': 'file',
        'active_sub_tab': 'liveStreaming',
        'process': 'Create'
    }
    return render(request, 'dashboards/create.html', context)

@has_permission(Role.LEVEL.admin)
def update_recording_files(request, id: int):
    recordingFile = RecordingFile.objects.filter(id=id).first()
    form = CreateLiveStreaming(data=request.POST or None,
                               instance=recordingFile,
                               user=request.user)
    if request.method == 'POST':
        if form.is_valid():
            files = form.save()
            messages.success(request, f'Update live streaming {files} success')
            return redirect(reverse('dashboards:files:index_livestreaming'))

    context = {
        'form': form,
        'title': 'Update Live Streaming',
        'active_tab': 'file',
        'active_sub_tab': 'liveStreaming',
        'process': 'Update'
    }
    return render(request,  'dashboards/files/create.html', context)


# ------------- Google Drive -------------
@has_permission(Role.LEVEL.admin)
def sync_file_from_googledrive(request):
    service = googledrive_service(request.user)
    query = f"mimeType = 'video/mpeg' or mimeType = 'video/mp4'"
    filesFields = 'id, name, webViewLink, webContentLink, permissions, createdTime, modifiedTime, mimeType'
    response = service.files().list(
        q=query,
        fields=f"nextPageToken, files({filesFields})",
        ).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')
    
    existingFiles = RecordingFile.objects.filter(is_from_gdrive=True, created_by=request.user).only('google_drive_id', 'id')
    existingGdriveIds = list(map(lambda file: file.google_drive_id, existingFiles))
    existingFilesObj = {}
    for extFile in existingFiles: existingFilesObj[extFile.google_drive_id] = extFile
    
    createFileList = []
    updateFileList = []
    for file in files:
        if (file.get('id') not in existingGdriveIds):
            createFile = RecordingFile(
                name=file.get('name'),
                created=file.get('createdTime'),
                updated=file.get('modifiedTime'),
                created_by=request.user,
                modified_by=request.user,
                url=file.get('webViewLink').replace("view", "preview"),
                google_drive_id=file.get('id'),
                type=RecordingFile.TYPE.file,
                is_from_gdrive=True
            )
            createFileList.append(createFile)
        else:
            updateFile = existingFilesObj[file.get('id')]
            updateFile.name = file.get('name')
            updateFile.url = file.get('webViewLink').replace("view", "preview")
            updateFileList.append(updateFile)
            del existingFilesObj[file.get('id')]
    
    if createFileList: RecordingFile.objects.bulk_create(createFileList)
    if updateFileList: RecordingFile.objects.bulk_update(updateFileList, ['name', 'url', 'is_from_gdrive'])
    if existingFilesObj:
        for key, value in existingFilesObj.items():
            RecordingFile.objects.get(id=value.id).delete()

    return redirect(reverse('dashboards:files:index'))