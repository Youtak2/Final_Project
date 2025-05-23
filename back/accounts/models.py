# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    asset = models.PositiveIntegerField(default=0)
    salary = models.PositiveIntegerField(default=0)
    age = models.PositiveIntegerField(default=0)
    saving_type = models.CharField(max_length=20, blank=True)
    invest_type = models.CharField(max_length=20, blank=True)
    main_bank = models.CharField(max_length=50, blank=True)

    followings = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        related_query_name='follower',
        blank=True
    )
