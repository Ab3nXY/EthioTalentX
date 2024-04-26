from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.urls import re_path
from  django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('accounts/profile/',views.profile, name='profile'),
    path('accounts/dashboard/',views.dashboard, name='dashboard'),
    path('', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('allauth.socialaccount.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]
