from django.shortcuts import render, redirect
from .models import Applicant

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def applicants_index(request):
    applicants = Applicant.objects.all()
    return render(request, 'applicants/index.html', {
        'applicants': applicants
    })