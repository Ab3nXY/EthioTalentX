from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile/',views.profile, name='profile'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('accounts/dashboard/',views.dashboard, name='dashboard'),
    path('accounts/profiles/',views.profiles, name='profiles'),
    path('accounts/add_experience/', views.ExperienceCreateView.as_view(), name='add_experience'),
    path('experiences/<int:pk>/', views.ExperienceDetailView.as_view(), name='experience_detail'),
    path('experiences/update/<int:pk>/', views.ExperienceUpdateView.as_view(), name='edit_experience'),
    path('experiences/delete/<int:pk>/', views.ExperienceDeleteView.as_view(), name='delete_experience'),
    path('accounts/add_education/',views.EducationCreateView.as_view(), name='add_education'),
    path('educations/<int:pk>/', views.EducationDetailView.as_view(), name='education_detail'),
    path('educations/update/<int:pk>/', views.EducationUpdateView.as_view(), name='edit_education'),
    path('educations/delete/<int:pk>/', views.EducationDeleteView.as_view(), name='delete_education'),
]