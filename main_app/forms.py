# from django import forms
from django.forms import ModelForm
from .models import SkillSet

class SkillSetForm(ModelForm):
    class Meta:
        model = SkillSet
        fields = ['skill']
        # widgets = {
        #     'skill': forms.TextInput(attrs={'class': 'border-gray-300 rounded px-3 py-1', 'placeholder': 'Enter skill'}),
        # }

  