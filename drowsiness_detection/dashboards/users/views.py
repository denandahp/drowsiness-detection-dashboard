from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from drowsiness_detection.apps.users.model import User
from drowsiness_detection.dashboards.users.forms import UpdateUser, UpdateConnection


def edit_user(request, id: int):
    user = User.objects.filter(id=id).first()
    form = UpdateUser(data=request.POST or None,
                      files=request.FILES or None,
                      instance=user)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Update user {user} success')
            return redirect(reverse('dashboards:users:edit_user',  kwargs={'id': user.id}))
        else:
            print(form.errors)

    context = {
        'form': form,
        'process': 'Update'
    }
    return render(request, 'dashboards/users/update.html', context)

def detail(request, id: int):
    user = get_object_or_404(User, id=id)
    context = {
        'title': 'Account',
        'data': user
    }
    return render(request, 'dashboards/files/detail.html', context)

def edit_connection(request, id: int):
    user = User.objects.filter(id=id).first()
    form = UpdateConnection(data=request.POST or None,
                            files=request.FILES or None,
                            instance=user,
                            user=user)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Update connection {user} success')
            return redirect(reverse('dashboards:users:edit_connection', kwargs={'id': user.id}))
        else:
            print(form.errors)

    context = {
        'form': form,
        'process': 'Update'
    }
    return render(request, 'dashboards/users/connections.html', context)