from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/<str:username>/', views.chatPage, name='chat_page'),
    path('api/user/<int:user_pk>/', views.user_detail, name='user_detail'),
    path('api/messages/<int:user_pk>/', views.messages_detail, name='messages_detail'),
]
