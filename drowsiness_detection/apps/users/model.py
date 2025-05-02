from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models import JSONField
from drowsiness_detection.core.utils import FilenameForPathGenerator
from model_utils import Choices


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    LEVEL = Choices(
        (1, "superuser", "Superuser"),
        (2, "admin", "Admin"),
        (3, "staff", "Staff"),
    )
    level = models.PositiveIntegerField(choices=LEVEL)

class CustomUserManager(UserManager):

    def create_user(self, email: str, password: str, type=None, **extra_fields: Any):
        """
        Creates and saves a User with the email and mobile_number.
        """
        user = self.model(email=email, is_superuser=False, is_staff=False, is_active=True,
                          **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.name = user.email
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ A user account that can login and access functionality.
    """

    email = models.EmailField('email address', unique=True, blank=False, null=False)
    is_guest = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)
    phone_number = models.CharField('phone number',
                                    blank=True, null=True,
                                    max_length=50)
    properties = JSONField(blank=True, null=True, verbose_name='properties')
    verified = models.BooleanField(default=True, verbose_name='verified')
    is_staff = models.BooleanField(default=False, verbose_name='is_staff')
    is_active = models.BooleanField(default=False, verbose_name='is_active')
    date_joined = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to=FilenameForPathGenerator('user_image'), blank=True, null=True)
    isAuthGDrive = models.BooleanField(default=False)

    def has_permission(self, role: str) -> bool:
        if hasattr(self, '_cached_permissions'):
            return role in self._cached_permissions  # type: ignore

        permission_codes = Role.objects.all().only('level').values_list('level',flat=True)
        self._cached_permissions = set(permission_codes)
        return role in self._cached_permissions
