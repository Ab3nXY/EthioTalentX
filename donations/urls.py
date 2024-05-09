from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_with_product, name='donate'),
    path('donation/success/', views.donation_success, name='donation_success'),
    path('donation/cancelled/', views.donation_cancelled, name='donation_cancelled'),
]
