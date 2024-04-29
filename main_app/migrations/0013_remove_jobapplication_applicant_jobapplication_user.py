# Generated by Django 5.0.4 on 2024-04-23 03:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0012_remove_jobapplication_user_jobapplication_applicant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='applicant',
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
