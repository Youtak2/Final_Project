# Generated by Django 4.2.11 on 2025-05-23 04:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_customuser_followings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='followings',
            field=models.ManyToManyField(blank=True, related_name='followers_set', related_query_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
