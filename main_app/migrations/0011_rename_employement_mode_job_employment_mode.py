# Generated by Django 5.0.4 on 2024-04-22 03:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_remove_jobapplication_applicant_jobapplication_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='employement_mode',
            new_name='employment_mode',
        ),
    ]
