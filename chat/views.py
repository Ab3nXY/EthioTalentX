from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage, ChatRoom

@login_required
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("account_login")

    user_to_chat_with = None
    username_to_chat = kwargs.get('username')
    if username_to_chat:
        try:
            user_to_chat_with = User.objects.get(username=username_to_chat)
        except User.DoesNotExist:
            pass  # Handle user not found

    chat_room = None
    if user_to_chat_with:
        chat_room_filters = {
            'users__in': [request.user, user_to_chat_with]
        }
        chat_rooms = ChatRoom.objects.filter(**chat_room_filters)
        if chat_rooms.exists():
            chat_room = chat_rooms.first()

    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message and chat_room:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=user_to_chat_with,
                room=chat_room,
                message=message
            )
            # Redirect back to the chat page after sending a message
            return redirect('chat_page', username=user_to_chat_with.username)

    chat_messages = None
    if chat_room:
        chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('-timestamp')

    if request.GET.get('clear_chat'):
        if chat_room and request.user.has_perm('clear_chat', chat_room):
            chat_room.messages.all().delete()  # Assuming messages are related to the chat room

    context = {
        'chat_room_id': chat_room.id if chat_room else None,
        'user_to_chat': user_to_chat_with,
        'chat_messages': chat_messages,
        'chat_room': chat_room,
        'can_clear_chat': request.user.has_perm('clear_chat', chat_room) if chat_room else False,
    }
    return render(request, "chat/chatPage.html", context)
