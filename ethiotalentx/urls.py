from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.urls import re_path
from  django.views.static import serve 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("chat.urls")),
    path('', include('accounts.urls')),
    path('', include('donations.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('allauth.socialaccount.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
]

# Serve static and media files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)