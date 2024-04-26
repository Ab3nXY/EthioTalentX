from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile',views.profile, name='profile'),
    path('accounts/dashboard',views.dashboard, name='dashboard'),
]