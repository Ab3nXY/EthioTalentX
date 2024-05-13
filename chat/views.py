from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Assuming User model for authentication
from .models import ChatMessage, ChatRoom

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("account_login")

    # Retrieve the user profile being viewed (optional argument)
    user_to_chat_with = None
    username_to_chat = kwargs.get('username')
    if username_to_chat:
        try:
            user_to_chat = User.objects.get(username=username_to_chat)
        except User.DoesNotExist:
            pass  # Handle user not found

    # Check if a ChatRoom already exists for these users
    chat_room = None
    if user_to_chat:
        chat_room_filters = {
            'users__in': [request.user, user_to_chat]
        }
        chat_rooms = ChatRoom.objects.filter(**chat_room_filters)
        if chat_rooms.exists():
            chat_room = chat_rooms.first()

    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message and chat_room:  # Ensure a chat room is available
            # Save the message to the database
            ChatMessage.objects.create(
                sender=request.user,
                receiver=user_to_chat,
                room=chat_room,
                message=message
            )

    # Retrieve chat messages for the room (if applicable)
    chat_messages = None
    if chat_room:
        chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('-timestamp')  # Order by most recent first

    # Handle clearing chat room (optional, implement logic as needed)
    if request.GET.get('clear_chat'):  # Add a GET parameter to trigger clearing
        if chat_room and request.user.has_perm('clear_chat', chat_room):  # Check permission to clear
            # Implement logic to clear chat messages from the room (e.g., delete messages)
            pass  # Replace with actual message deletion code

    context = {
        'chat_room_id': chat_room.id if chat_room else None,
        'user_to_chat': user_to_chat,
        'chat_messages': chat_messages,
        'chat_room': chat_room,
        # Add a flag or mechanism to indicate if chat room clearing is allowed
        'can_clear_chat': request.user.has_perm('clear_chat', chat_room) if chat_room else False,
    }
    return render(request, "chat/chatPage.html", context)
