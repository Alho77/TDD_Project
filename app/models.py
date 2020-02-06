from django.conf import settings
from django.contrib.auth.models import (AbstractUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Create user with email instead of username"""

        if email is None:
            raise ValueError('Invalid email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """Custom user model that support email instead of username"""
    username = models.CharField(blank=True, null=True, error_messages={'unique': 'A user with that username already exists.'},
                                max_length=150, unique=True, validators=[UnicodeUsernameValidator()], verbose_name='username')
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Tag(models.Model):
    """Assign tag to user"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
