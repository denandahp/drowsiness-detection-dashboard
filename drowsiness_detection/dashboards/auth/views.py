from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login, logout
from django.urls import reverse

from drowsiness_detection.core.services.google import googledrive_service
from drowsiness_detection.dashboards.auth.forms import UserRegistration, LoginAuthForm


def login_dashboards(request):
    form = LoginAuthForm(data=request.POST or None)
    if request.method == 'POST':
        next_page = request.GET.get('next', None)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if next_page:
                return redirect(next_page)
            # if user.is_superuser:
            #     return redirect('backoffices:partners:index')
            else:
                return redirect('dashboards:files:index')
        else:
            print(form.errors)
            messages.error(request, 'Email atau Sandi salah.')

    context = {'form': form}
    return render(request, 'dashboards/auth/login.html', context)

def logout_dashboards(request):
    logout(request)
    return redirect('auth:login')

def signup(request):
    form = UserRegistration(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            site = form.save()
            messages.success(request, f'Create files {site} success')
            return redirect(reverse('auth:login'))
        else:
            print(form.errors)

    context = {
        'form': form
    }
    return render(request, 'dashboards/auth/signup.html', context)

def googledrive_auth(request):
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
    