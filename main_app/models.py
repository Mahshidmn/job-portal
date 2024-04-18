from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

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
    description = models.TextField()

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
    expiration_date = models.DateField(null=True, blank=True)

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