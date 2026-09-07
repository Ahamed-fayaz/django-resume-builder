from django.contrib import admin
from django.urls import path, include
from resume import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('accounts.urls')),

    path('', views.resume_list, name='resume_list'),

    # Resume
    path('addresume/', views.resume, name='resume'),
    path('resumedetail/<int:id>/', views.resume_detail, name='resume_detail'),
    path('editresume/<int:id>/', views.edit_resume, name='edit_resume'),
    path('deleteresume/<int:id>/', views.delete_resume, name='delete_resume'),

    # Education
    path('addeducation/<int:id>/', views.add_ed, name='add_ed'),
    path('editeducation/<int:id>/', views.edit_ed, name='edit_ed'),
    path('deleteeducation/<int:id>/', views.del_ed, name='del_ed'),

    # Projects
    path('addproject/<int:id>/', views.add_proj, name='add_proj'),
    path('editproject/<int:id>/', views.edit_proj, name='edit_proj'),
    path('deleteproject/<int:id>/', views.del_proj, name='del_proj'),

    # Experience
    path('addexperience/<int:id>/', views.add_exp, name='add_exp'),
    path('editexperience/<int:id>/', views.edit_exp, name='edit_exp'),
    path('deleteexperience/<int:id>/', views.del_exp, name='del_exp'),

    # Skills
    path('addskill/<int:id>/', views.add_skills, name='add_skills'),
    path('editskill/<int:id>/', views.edit_skills, name='edit_skills'),
    path('deleteskill/<int:id>/', views.delete_skills, name='delete_skills'),

    # Certifications
    path('addcertifications/<int:id>/', views.add_certs, name='add_certs'),
    path('editcertifications/<int:id>/', views.edit_certs, name='edit_certs'),
    path('deletecertifications/<int:id>/', views.delete_certs, name='delete_certs'),

    # Languages
    path('addlanguage/<int:id>/', views.add_lan, name='add_lan'),
    path('editlanguage/<int:id>/', views.edit_lan, name='edit_lan'),
    path('deletelanguage/<int:id>/', views.delete_lan, name='delete_lan'),

    # Preview / PDF
    path('resumepreview/<int:id>/', views.resume_preview, name='resume_preview'),
    path('resumepdf/<int:id>/', views.resume_pdf, name='resume_pdf'),
]