from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile/',views.profile, name='profile'),
    path('accounts/dashboard/',views.dashboard, name='dashboard'),
    path('accounts/profiles/',views.profiles, name='profiles'),
    path('accounts/add_experience/',views.add_experience, name='add_experience'),
    path('accounts/add_education/',views.add_education, name='add_education')
]