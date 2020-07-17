from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def creat_user(self, email, password=None, *args, **kwargs):
        if "gmail.com" not in email:
            raise ValidationError('gmail.com shold be in email')
        user = 