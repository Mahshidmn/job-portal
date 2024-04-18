import os
import uuid
import boto3

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Applicant, Photo, Resume

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .forms import SkillSetForm



######## Applicant CRUD ############
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class ApplicantList(ListView):
    model = Applicant


def applicants_detail(request, applicant_id):
   applicant = Applicant.objects.get(id=applicant_id)
   skillset_form = SkillSetForm()
   return render(request, 'main_app/applicant_detail.html', {
      'applicant': applicant, 
      'skillset_form': skillset_form,
   })

class ApplicantCreate(CreateView):
    model = Applicant
    fields = ['name', 'title', 'email', 'phone_number', 'location', 'summary', 'linkedin_profile_url', 'portfolio_url', 'availability']
    
    def form_valid(self, form):
      # self.request.user is the logged user, remeber user object is available when we login
        form.instance.user = self.request.user
      # let the CreateView's form_valid method
      #do its regular work which is saving the model in DB & redirect
        return super().form_valid(form)
    
######## Skillset CRUD ###########

def add_skillset(request, applicant_id):
   skillset_form = SkillSetForm(request.POST) # request.POST is equivalent for req.body
   if skillset_form.is_valid():
      new_skillset = skillset_form.save(commit=False)
      new_skillset.applicant_id = applicant_id
      new_skillset.save()
   return redirect('detail', applicant_id=applicant_id)
      

    
######## Photo CRUD ###########

def add_photo(request, applicant_id):
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      # Need a unique 'key' (filename)
      # It needs to keep the same file extension
      # of the file that was uploaded(.png, .jpeg, etc)
      # First part of this command generate a unique identifier +
      # and second part finds the . in the file name(ex: cat01.png and slice .png using : until the end)
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
         bucket = os.environ['S3_BUCKET']
         s3.upload_fileobj(photo_file, bucket, key)
         #Build the full url string
         url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
         Photo.objects.create(url=url, applicant_id=applicant_id)
      except Exception as e:
         print('An error occurred uploading file to S3')
         print(e)
   return redirect('detail', applicant_id=applicant_id)

######## Resume CRUD ###########
def add_resume(request, applicant_id):
   resume_file = request.FILES.get('resume-file', None)
   if resume_file:
      print('file found')
      s3 = boto3.client('s3')
      # Need a unique 'key' (filename)
      # It needs to keep the same file extension
      # of the file that was uploaded(.png, .jpeg, etc)
      # First part of this command generate a unique identifier +
      # and second part finds the . in the file name(ex: cat01.png and slice .png using : until the end)
      key = uuid.uuid4().hex[:6] + resume_file.name[resume_file.name.rfind('.'):]
      try:
         bucket = os.environ['S3_BUCKET']
         s3.upload_fileobj(resume_file, bucket, key)
         #Build the full url string
         url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
         Resume.objects.create(url=url, applicant_id=applicant_id)
      except Exception as e:
         print('An error occurred uploading file to S3')
         print(e)
   return redirect('detail', applicant_id=applicant_id)


def signup(request):
   error_message = ''
   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         # save the user in DB
         user = form.save()
         # Authomatically log in the new user
         login(request, user)
         return redirect('index') # redirect send a GET request
      else:
         error_message = 'Invalid sign up - try again'
    #  # A bad POST or a GET request, so render signup.html with an empty form
   form = UserCreationForm()
   context = {'form': form, 'error_message': error_message}
   return render(request, 'registration/signup.html', context)
()