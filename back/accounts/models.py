# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    asset = models.PositiveIntegerField(default=0)
    salary = models.PositiveIntegerField(default=0)
    age = models.PositiveIntegerField(default=0)  # 👈 추가
