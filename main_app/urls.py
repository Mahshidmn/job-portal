from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('applicants/', views.ApplicantList.as_view(), name='index'),
    path('applicants/<int:applicant_id>/', views.applicants_detail, name='detail'),
    path('applicants/<int:applicant_id>/add_skillset/', views.add_skillset, name='add_skillset'),
    path('applicants/<int:applicant_id>/add_photo/', views.add_photo, name='add_photo'),
    path('applicants/<int:applicant_id>/add_resume/', views.add_resume, name='add_resume'),
    path('applicants/create/', views.ApplicantCreate.as_view(), name='applicants_create'),
    path('accounts/signup/', views.signup, name='signup'),
 ]