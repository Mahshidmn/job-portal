from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('applicants/', views.ApplicantList.as_view(), name='index'),
    path('applicants/<int:applicant_id>/', views.applicants_detail, name='detail'),
    path('applicants/<int:applicant_id>/add_skillset/', views.add_skillset, name='add_skillset'),
    path('applicants/<int:applicant_id>/add_workexperience/', views.add_workexperience, name='add_workexperience'),
    path('applicants/<int:applicant_id>/add_education/', views.add_education, name='add_education'),
    path('applicants/<int:applicant_id>/add_certification/', views.add_certification, name='add_certification'),
    path('applicants/<int:applicant_id>/add_photo/', views.add_photo, name='add_photo'),
    path('applicants/<int:applicant_id>/add_resume/', views.add_resume, name='add_resume'),
    path('applicants/create/', views.ApplicantCreate.as_view(), name='applicants_create'),
    path('applicants/<int:pk>/update/', views.ApplicantUpdate.as_view(), name='applicants_update'),
    path('applicants/<int:pk>/delete/', views.ApplicantDelete.as_view(), name='applicants_delete'),
    path('accounts/signup/', views.signup, name='signup'),
 ]