from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (PermissionsMixin, UserManager, AbstractBaseUser)
from django.utils.translation import gettext_lazy
import jwt
from datetime import timedelta
from django.utils import timezone
from uuid import uuid4 as uuid
from todo.settings import SECRET_KEY, ENCRYPTION_ALGORITHM

class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    id = models.UUIDField(default=uuid, primary_key=True)
    username = models.CharField(
        gettext_lazy('username'),
        max_length=100,
        unique=True,
        help_text=gettext_lazy('Required. 100 characters or fewer. Letters,') ,
        validators=[username_validator],
        error_messages={'unique': gettext_lazy("A user with that username already exists."),},
    )
    email = models.EmailField(gettext_lazy('email address'), blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(default=None, null=True)
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def token(self):
        token = jwt.encode({'username': self.username, 'email': self.email, 'exp': timezone.now() + timedelta(hours=24)}, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)
        return token