from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:username>/', views.chatPage, name='chat_page'),
    path('api/user/<int:user_pk>/', views.user_detail, name='user_detail'),
    path('api/messages/<int:user_pk>/<int:room_id>/', views.messages_detail, name='messages_detail'),
    path('api/fetch-chat-rooms/', views.fetch_chat_rooms, name='fetch_chat_rooms'),
    path('api/create-chat-room/', views.create_chat_room, name='create_chat_room'),
    path('api/check-chat-room/<int:user_id>/', views.check_chat_room, name='check_chat_room'),
]
