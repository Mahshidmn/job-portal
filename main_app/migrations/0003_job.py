# Generated by Django 5.0.4 on 2024-04-19 07:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_recruiter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('company', models.CharField(max_length=500)),
                ('location', models.CharField(max_length=500)),
                ('job_type', models.CharField(choices=[('O', 'Onsite'), ('H', 'Hybrid'), ('R', 'Remote')], default='O', max_length=1)),
                ('employement_mode', models.CharField(choices=[('F', 'Full Time'), ('P', 'Part Time'), ('C', 'Contract')], default='F', max_length=1)),
                ('description', models.TextField()),
                ('salary', models.IntegerField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('recruiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.recruiter')),
            ],
        ),
    ]
