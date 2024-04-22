from django.contrib import admin
from .models import Applicant, JobApplication, Job, Recruiter

admin.site.register(Applicant)
admin.site.register(Recruiter)
admin.site.register(JobApplication)
admin.site.register(Job)
