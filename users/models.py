from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from .managers import UserManager
from helpers.models import BaseModel
from django.db import models
from pyotp import random_base32

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    name = models.CharField(max_length=200, blank=False)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField("staff status", default=False)
    is_superuser = models.BooleanField("Superuser", default=False)
    enable_two_factor_authentication = models.BooleanField(default=False)
    two_fa_identifier = models.CharField(max_length=50, editable=False, default=random_base32)

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def get_basic_info(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "email": self.email
        }
