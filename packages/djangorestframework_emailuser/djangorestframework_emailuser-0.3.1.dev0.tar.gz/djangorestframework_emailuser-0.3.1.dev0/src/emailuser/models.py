from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .managers import EmailUserManager


class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True, db_index=True)
    name = models.CharField(max_length=40)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def get_full_name(self):
        return str(self)

    get_short_name = get_full_name

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class EmailUser(AbstractEmailUser):
    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
