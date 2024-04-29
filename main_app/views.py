import os
import uuid
import boto3

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Applicant, Recruiter, Photo, Resume, Job, JobApplication
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib import messages

from .forms import SkillSetForm, WorkExperienceForm, EducationForm, CertificationForm



######## Applicant CRUD ############
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


@login_required
def applicants_index(request):
    applicants = Applicant.objects.all()
    return render(request,'main_app/applicant_list.html', {
       'applicants': applicants,
    })


@login_required
def applicants_detail(request, applicant_id):
   applicant = Applicant.objects.get(id=applicant_id)
   skillset_form = SkillSetForm()
   workexperience_form = WorkExperienceForm()
   education_form = EducationForm()
   certification_form = CertificationForm()
   return render(request, 'main_app/applicant_detail.html', {
      'applicant': applicant, 
      'skillset_form': skillset_form,
      'workexperience_form': workexperience_form,
      'education_form': education_form,
      'certification_form': certification_form,
   })

class ApplicantCreate(LoginRequiredMixin, CreateView):
    model = Applicant
    fields = ['name', 'title', 'email', 'phone_number', 'location', 'summary', 'linkedin_profile_url', 'portfolio_url', 'availability']
    
    def form_valid(self, form):
      # self.request.user is the logged user, remeber user object is available when we login
        form.instance.user = self.request.user
      # let the CreateView's form_valid method
      #do its regular work which is saving the model in DB & redirect
        return super().form_valid(form)
    
class ApplicantUpdate(LoginRequiredMixin, UpdateView):
   model = Applicant
   fields = ['name', 'title', 'email', 'phone_number', 'location', 'summary', 'linkedin_profile_url', 'portfolio_url', 'availability']


class ApplicantDelete(LoginRequiredMixin, DeleteView):
   model = Applicant
   success_url = '/applicants/'
    
######## Skillset CRUD ###########
@login_required
def add_skillset(request, applicant_id):
   skillset_form = SkillSetForm(request.POST) # request.POST is equivalent for req.body
   if skillset_form.is_valid():
      new_skillset = skillset_form.save(commit=False)
      new_skillset.applicant_id = applicant_id
      new_skillset.save()
   return redirect('detail', applicant_id=applicant_id)


########## Work Experience CRUD ##############

def add_workexperience(request, applicant_id):
   workexperience_form = WorkExperienceForm(request.POST)
   print('add work experience')
   if workexperience_form.is_valid():
      new_workexperience = workexperience_form.save(commit=False)
      new_workexperience.applicant_id = applicant_id
      new_workexperience.save()
   else:
      print(workexperience_form.errors)
   return redirect('detail', applicant_id=applicant_id)
      

########## Education CRUD ##############
@login_required
def add_education(request, applicant_id):
   education_form = EducationForm(request.POST)
   if education_form.is_valid():
      new_education = education_form.save(commit=False)
      new_education.applicant_id = applicant_id
      new_education.save()
   return redirect('detail', applicant_id=applicant_id)


########## Certification CRUD ##############
@login_required
def add_certification(request, applicant_id):
   certification_form = CertificationForm(request.POST)
   if certification_form.is_valid():
      new_certification = certification_form.save(commit=False)
      new_certification.applicant_id = applicant_id
      new_certification.save()
   return redirect('detail', applicant_id=applicant_id)

    
######## Photo CRUD ###########
@login_required
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
@login_required
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

########## Job CRUD ################

class JobList(LoginRequiredMixin, ListView):
   model = Job

@login_required
def jobs_detail(request, pk):
    if JobApplication.objects.filter(user=request.user, job=pk).exists():
       has_applied = True
    else: 
       has_applied = False
    job = Job.objects.get(pk=pk)
    context = {'job': job, 'has_applied': has_applied}
    return render(request, 'main_app/jobs_detail.html', context)


class JobCreate(LoginRequiredMixin, CreateView):
   model = Job
   fields = '__all__'
   
   def get_success_url(self):
        return reverse('recruiter_dashboard')

class JobUpdate(LoginRequiredMixin, UpdateView):
   model = Job
   fields = '__all__'
   success_url = '/accounts/recruiter_dashboard/'

class JobDelete(LoginRequiredMixin, DeleteView):
   model = Job
   success_url = '/recruiter_dashboard/'  #TODO: dont hardcode ---use Reverse


########## Job Application CRUD ################
# Create a job application
@login_required
def apply_to_job(request, pk):
   if request.user.is_authenticated and request.user.is_applicant:
        job = Job.objects.get(pk=pk)
        # if the applicant try to apply to the same job again by entering jobs/<int:pk>/apply-to-job/'
        # the request should be blocked
        if JobApplication.objects.filter(user=request.user, job=pk).exists():
            messages.warning(request, 'Permission Denied')
            return redirect('applicant_dashboard')
        else:
            JobApplication.objects.create(
                job=job,
                user = request.user,
                status = 'Submitted'
            )
            messages.info(request, 'You have successfully applied! Please see applicant dashboard.')
            return redirect('applicant_dashboard')
   else:
      messages.info(request, 'Please log in to continue')
      return redirect('login')
   
# Get all the Job Applicants
@login_required
def all_job_applicants(request, pk):
   job = Job.objects.get(pk=pk)
   job_applications = job.jobapplication_set.all()
   print(job_applications)
   context = {'job': job, 'job_applications': job_applications}
   return render(request, 'main_app/all_job_applicants.html', context)


@login_required
def applied_jobs(request):
   job_applications = JobApplication.objects.filter(user=request.user)
   print(job_applications)
   return render(request, 'dashboard/applicant_dashboard.html', {
      'job_applications': job_applications,
   })


###### authentication and Registeration CRUD ########

# register applicant only
def register_applicant(request):
   error_message = ''
   if request.method == 'POST':
      form = RegisterUserForm(request.POST)
      if form.is_valid():
         # save the user in DB
         user = form.save(commit=False)
         user.is_applicant = True
         user.save()

         applicant = Applicant(
                name=request.POST.get('name'),
                title=request.POST.get('title'),
                email=request.POST.get('email'),
                phone_number=request.POST.get('phone_number'),
                location=request.POST.get('location'),
                summary=request.POST.get('summary'),
                linkedin_profile_url=request.POST.get('linkedin_profile_url'),
                portfolio_url=request.POST.get('portfolio_url'),
                availability=request.POST.get('availability')
            )
         applicant.user = user
         applicant.save()
         # Authomatically log in the new user
         login(request, user)
         return redirect('applicant_dashboard') # redirect send a GET request
      else:
         error_message = 'Invalid sign up - try again'
         print(form.errors)
         return redirect('register_applicant')
    #  # A bad POST or a GET request, so render signup.html with an empty form
   form = RegisterUserForm()
   context = {'form': form, 'error_message': error_message}
   return render(request, 'registration/register_applicant.html', context)



# register recruiter only
def register_recruiter(request):
   error_message = ''
   if request.method == 'POST':
      form = RegisterUserForm(request.POST)
      if form.is_valid():
         # save the user in DB
         user = form.save(commit=False)
         user.is_recruiter = True
         user.save()

         recruiter = Recruiter(
                name=request.POST.get('name'),
                title=request.POST.get('title'),
                email=request.POST.get('email'),
                phone_number=request.POST.get('phone_number'),
                company=request.POST.get('company')
         )
         recruiter.user = user
         recruiter.save()
         # Authomatically log in the new user
         login(request, user)
         return redirect('recruiter_dashboard') # redirect send a GET request
      else:
         error_message = 'Invalid sign up - try again'
         print(form.errors)
         return redirect('register_recruiter')
    #  # A bad POST or a GET request, so render signup.html with an empty form
   form = RegisterUserForm()
   context = {'form': form, 'error_message': error_message}
   return render(request, 'registration/register_recruiter.html', context)


# Login a user
def login_user(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      user = authenticate(request, username=username, password=password)
      if user is not None and user.is_active:
         login(request, user)
         if request.user.is_applicant:
            return redirect('applicant_dashboard')
         elif request.user.is_recruiter:
            return redirect('recruiter_dashboard')
         else:
            return redirect('login')
      else:
         messages.warning(request, 'Something went wrong')
         return redirect('login')
   else: 
      return render(request, 'registration/login.html')
   
# Logout a user
def logout_user(request):
   logout(request)
   messages.info(request, 'Your session has ended.')
   return redirect('login')


@login_required  
def proxy(request):
   if request.user.is_applicant:
      return redirect('applicant_dashboard')
   elif request.user.is_recruiter:
    return redirect('recruiter_dashboard')
   else:
      return redirect('login')
   

@login_required     
def applicant_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    if request.user.is_applicant:  # Use the is_applicant boolean field to check user role
        job_applications = JobApplication.objects.filter(user=request.user)
        return render(request, 'dashboard/applicant_dashboard.html', {'job_applications': job_applications})
    else:
        return redirect('recruiter_dashboard')
@login_required
def recruiter_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    if request.user.is_recruiter:  # Use the is_recruiter boolean field to check user role
        jobs = Job.objects.filter(recruiter=request.user.recruiter)
        return render(request, 'dashboard/recruiter_dashboard.html', {'jobs': jobs})
    else:
        return redirect('applicant_dashboard')

