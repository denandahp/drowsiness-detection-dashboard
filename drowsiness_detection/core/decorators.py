from typing import Callable, Any
from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login

from django.http import HttpResponse
from django.shortcuts import redirect


def has_permission(role: int) -> Callable:
    def _permission_decorator(view_func: Callable) -> Callable:
        @wraps(view_func)
        def _check_user_account(request, *args: Any, **kwargs: Any) -> HttpResponse:
            if not request.user.is_authenticated:
                messages.info(request, 'Please login as a user with privileges to view this page.')
                return redirect_to_login(request.path_info)

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            has_permission = request.user.has_permission(role)
            if has_permission:
                return view_func(request, *args, **kwargs)

            messages.info(request, 'Please login as a user with privileges to view this page.')

            # Try to login to refering page back, if not possible, redirect to login
            referrer = request.META.get('HTTP_REFERER')
            if referrer:
                return redirect('backoffices:orders:index')
            return redirect_to_login(request.path_info)
        return _check_user_account
    return _permission_decorator