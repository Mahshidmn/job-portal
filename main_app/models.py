from django.db import models
from django.urls import reverse

class Applicant(models.Model):
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    contactnumber = models.IntegerField()
    address = models.CharField(max_length=256)
    summary = models.CharField(max_length=1024)
    skillset = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'applicant_id': self.id})


# class Photo(models.Model):
#     url = models.CharField(max_length=200)
#     applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"Photo for applicant_id: {self.applicant_id} @{self.url}"dr