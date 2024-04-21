from django.conf import settings
from django.db import models
from django.urls import reverse

from django.contrib.auth.models import AbstractUser

SKILLS = (
    ('H', 'HTML'),
    ('C', 'CSS'),
    ('J', 'Javascript'),
    ('N', 'Node.js'),
    ('R', 'React'),
    ('E', 'Express'),
    ('P', 'Python'),
    ('D', 'Django'),
    ('M', 'MongoDB'),
    ('S', 'SQL'),
)

JOB_TYPES = (
    ('O', 'Onsite'),
    ('H', 'Hybrid'),
    ('R', 'Remote'),
)

EPLOYEMENT_MODES = (
    ('F', 'Full Time'),
    ('P', 'Part Time'),
    ('C', 'Contract'),
)




class User(AbstractUser):
    # email = models.EmailField(unique=True)
    username = models.CharField(max_length=256, unique=True)
    is_recruiter = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=15)
    company = models.CharField(max_length=256)

    def __str__(self):
        return self.name
    
    

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=15)
    location = models.CharField()
    summary = models.TextField(max_length=1024)
    linkedin_profile_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    availability = models.DateField()

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'applicant_id': self.id})
    
class SkillSet(models.Model):
    skill = models.CharField(
        max_length=1,
        choices = SKILLS,
        default = SKILLS[0][0]   
    )
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):      
         return f"{ self.get_skill_display() }"
    

class WorkExperience(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allows for current employment
    

    def __str__(self):
        return f'{self.job_title} at {self.company}'
    
    
    
class Education(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    institute = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Allows for current studies
    location = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.degree} from {self.institute}'
    

class Certification(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    date_awarded = models.DateField()

    def __str__(self):
        return f'{self.name} from {self.issuing_organization}'

    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for applicant_id: {self.applicant_id} @{self.url}"
    
class Resume(models.Model):
    url = models.CharField(max_length=200)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

    def __str__(self):
        return f"Resume for applicant_id: {self.applicant_id} @{self.url}"
    

class Job(models.Model):
    job_title = models.CharField(max_length=500)
    company = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    job_type = models.CharField(
        max_length=1,
        choices = JOB_TYPES,
        default = JOB_TYPES[0][0]   
    )
    employement_mode = models.CharField(
        max_length=1,
        choices = EPLOYEMENT_MODES,
        default = EPLOYEMENT_MODES[0][0]   
    )
    about_company = models.TextField()
    job_requirements = models.TextField()
    ideal_candidate = models.TextField()
    salary = models.IntegerField()
    posted_on = models.DateField(auto_now_add=True)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('jobs_detail', kwargs={'pk': self.id }) # pk is equal to toy.id, Django prefers pk
    
    def __str__(self):
        return self.job_title
    


class JobApplication(models.Model):
    status_choices = (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Submitted', 'Submitted'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return f'{self.user.applicant.name} for {self.job.job_title} - {self.status}'
