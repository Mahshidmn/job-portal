# from django import forms
from django.forms import ModelForm
from .models import SkillSet, WorkExperience, Education, Certification

class SkillSetForm(ModelForm):
    class Meta:
        model = SkillSet
        fields = ['skill']
        # widgets = {
        #     'skill': forms.TextInput(attrs={'class': 'border-gray-300 rounded px-3 py-1', 'placeholder': 'Enter skill'}),
        # }

class WorkExperienceForm(ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company', 'job_title', 'start_date', 'end_date']


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['institute', 'degree', 'start_date', 'end_date', 'location']


class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_organization', 'date_awarded']