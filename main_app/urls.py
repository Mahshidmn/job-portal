from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('applicants/', views.applicants_index, name='index'),
    path('applicants/<int:applicant_id>/', views.applicants_detail, name='detail'),
    path('applicants/<int:applicant_id>/add_skillset/', views.add_skillset, name='add_skillset'),
    path('applicants/<int:applicant_id>/add_workexperience/', views.add_workexperience, name='add_workexperience'),
    path('applicants/<int:applicant_id>/add_education/', views.add_education, name='add_education'),
    path('applicants/<int:applicant_id>/add_certification/', views.add_certification, name='add_certification'),
    path('applicants/<int:applicant_id>/add_photo/', views.add_photo, name='add_photo'),
    path('applicants/<int:applicant_id>/add_resume/', views.add_resume, name='add_resume'),
    path('applicants/create/', views.ApplicantCreate.as_view(), name='applicants_create'),
    path('applicants/<int:pk>/update/', views.ApplicantUpdate.as_view(), name='applicant_update'),
    path('applicants/<int:pk>/delete/', views.ApplicantDelete.as_view(), name='applicant_delete'),
    path('applicants/applied_jobs/', views.applied_jobs, name='applied_jobs'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/register_applicant/', views.register_applicant, name='register_applicant'),
    path('accounts/register_recruiter/', views.register_recruiter, name='register_recruiter'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    
    path('proxy/', views.proxy, name='proxy'),
    path('applicant_dashboard/', views.applicant_dashboard, name='applicant_dashboard'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

    path('jobs/', views.JobList.as_view(), name='jobs_index'),
    path('jobs/<int:pk>/', views.jobs_detail, name='jobs_detail'),
    path('jobs/create/', views.JobCreate.as_view(), name='jobs_create'),
    path('jobs/<int:pk>/update/', views.JobUpdate.as_view(), name='jobs_update'),
    path('jobs/<int:pk>/delete/', views.JobDelete.as_view(), name='jobs_delete'),
    path('jobs/<int:pk>/apply_to_job/', views.apply_to_job, name='apply_to_job'),
    path('jobs/<int:pk>/all_job_applicants/', views.all_job_applicants, name='all_job_applicants'),
    

 ]