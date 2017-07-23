from django.contrib import auth
from django.db import models
import uuid

# Create your models here.

# Workaround for auth login
auth.signals.user_logged_in.disconnect(auth.models.update_last_login)


class User(models.Model):
    '''A Minimal User Model'''
    email = models.EmailField(primary_key=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    '''Generate UID for email'''
    email = models.EmailField(default='')
    uid = models.CharField(default=uuid.uuid4, max_length=40)
