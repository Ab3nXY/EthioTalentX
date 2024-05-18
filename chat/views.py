from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatMessage, ChatRoom
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.http import JsonResponse
from accounts.models import Profile
from .models import ChatMessage
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST 
import json

@login_required
def user_detail(request, user_pk):
    print(f"Fetching details for user with PK: {user_pk}")  # Debug statement
    user = get_object_or_404(User, pk=user_pk)
    print(f"User found: {user.username}")  # Debug statement
    profile = get_object_or_404(Profile, user=user)
    print(f"Profile found for user: {profile}")  # Debug statement
    user_data = {
        'id': user.id,
        'username': user.username,
        'image': request.build_absolute_uri(profile.image.url) if profile.image else '',
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    print(f"User data to be returned: {user_data}")  # Debug statement
    return JsonResponse(user_data)

@login_required
def messages_detail(request, user_pk, room_id):
    user_to_chat_with = get_object_or_404(User, pk=user_pk)
    current_user = request.user
    
    # Debug statements
    print(f"Current User: {current_user.username} (ID: {current_user.id})")
    print(f"Chatting with: {user_to_chat_with.username} (ID: {user_to_chat_with.id})")
    print(f"Chat room = {room_id}")
    
    # Fetch chat room based on room_id
    chat_room = get_object_or_404(ChatRoom, pk=room_id)
    
    # Fetch messages for the chat room
    chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')
    
    messages_data = []
    for message in chat_messages:
        print(f"Message from {message.sender.username} to {message.receiver.username}: {message.message}")
        message_data = {
            'sender_id': message.sender.id,
            'sender_username': message.sender.username,
            'receiver_id': message.receiver.id,
            'receiver_username': message.receiver.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        messages_data.append(message_data)
    
    return JsonResponse(messages_data, safe=False)


@login_required
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("account_login")

    user_to_chat_with = None
    username_to_chat = kwargs.get('username')
    
    # Fetch the user to chat with based on username
    if username_to_chat:
        try:
            user_to_chat_with = User.objects.get(username=username_to_chat)
        except User.DoesNotExist:
            print(f"User with username '{username_to_chat}' does not exist.")  # Debugging print
            return HttpResponseNotFound("User not found")

    # Ensure both users are fetched and valid
    if request.user and user_to_chat_with:
        # Check if a chat room exists between the current user and the user to chat with
        chat_room = ChatRoom.objects.filter(users=request.user).filter(users=user_to_chat_with).first()

        # If no chat room exists, create a new one
        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.users.add(request.user, user_to_chat_with)

    else:
        return HttpResponseBadRequest("Invalid users")

    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message and chat_room:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=user_to_chat_with,
                room=chat_room,
                message=message
            )
            print(f"Message sent from {request.user.username} to {user_to_chat_with.username}: {message}")  # Debugging print
            # Redirect back to the chat page after sending a message
            return redirect('chat_page', username=user_to_chat_with.username)

    chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('-timestamp') if chat_room else None

    if request.GET.get('clear_chat'):
        if chat_room and request.user.has_perm('clear_chat', chat_room):
            chat_room.messages.all().delete()  # Assuming messages are related to the chat room
            print(f"Chat messages cleared by {request.user.username} in chat room {chat_room.id}")  # Debugging print

    # Fetch latest chat rooms for the current user
    user_chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-last_message_time')

    # Prepare user data for chat modal
    user_data = {
        'id': user_to_chat_with.pk,
        'username': user_to_chat_with.username,
        'email': user_to_chat_with.email,
        'company': user_to_chat_with.company,
        'website': user_to_chat_with.website,
        'location': user_to_chat_with.location,
        'bio': user_to_chat_with.bio,
        'githubusername': user_to_chat_with.githubusername,
        'date': user_to_chat_with.date.strftime('%Y-%m-%d %H:%M:%S'),
        'image_url': user_to_chat_with.image.url if user_to_chat_with.image else '',
        'occupation': user_to_chat_with.occupation,
        'skills': list(user_to_chat_with.skills.values_list('name', flat=True))
    }

    context = {
        'chat_room_id': chat_room.id if chat_room else None,
        'user_to_chat': user_to_chat_with,
        'chat_messages': chat_messages,
        'chat_room': chat_room,
        'can_clear_chat': request.user.has_perm('clear_chat', chat_room) if chat_room else False,
        'user_chat_rooms': user_chat_rooms,
        'user_data': user_data,  # Pass user data directly to template
    }
    return render(request, "chat/chatPage.html", context)


@login_required
def chat_list(request):
    # Fetch latest chat rooms for the current user
    user_chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-last_message_time')

    context = {
        'user_chat_rooms': user_chat_rooms,
    }
    return render(request, "chat/chat_list.html", context)

@login_required
@require_POST
def create_chat_room(request):
    data = json.loads(request.body)
    user_id_1 = data.get('user_id_1')
    user_id_2 = data.get('user_id_2')

    if not user_id_1 or not user_id_2:
        return JsonResponse({'error': 'Invalid user_id provided'}, status=400)

    # Fetch the users to chat with
    user1 = get_object_or_404(User, pk=user_id_1)
    user2 = get_object_or_404(User, pk=user_id_2)

    # Ensure the chat room doesn't already exist between these two users
    existing_chat_room = ChatRoom.objects.filter(users=user1).filter(users=user2).first()
    if existing_chat_room:
        return JsonResponse({'room_id': existing_chat_room.pk})

    # Generate room name based on usernames (example: concatenation)
    room_name = f"{user1.username}_{user2.username}"

    # Create a new chat room
    chat_room = ChatRoom.objects.create(name=room_name)

    # Add users to the chat room
    chat_room.users.add(user1, user2)
    chat_room.save()

    return JsonResponse({'room_id': chat_room.pk})


@login_required
def check_chat_room(request, user_id):
    user_to_chat_with = get_object_or_404(User, pk=user_id)
    chat_room = ChatRoom.objects.filter(users=request.user).filter(users=user_to_chat_with).first()
    if chat_room:
        return JsonResponse({'exists': True, 'room_id': chat_room.pk})
    else:
        return JsonResponse({'exists': False})
