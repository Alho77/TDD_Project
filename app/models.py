from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create user with email instead of username"""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
