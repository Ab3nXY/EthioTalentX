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
import logging
from django.db.models import Max

@login_required
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    profile = get_object_or_404(Profile, user=user)
    user_data = {
        'id': user.id,
        'username': user.username,
        'image': request.build_absolute_uri(profile.image.url) if profile.image else '',
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return JsonResponse(user_data)

logger = logging.getLogger(__name__)

@login_required
def messages_detail(request, user_pk, room_id):
    if request.method == 'GET':
        # Fetch chat room based on room_id
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        
        # Fetch messages for the chat room
        chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('timestamp')
        
        messages_data = []
        for message in chat_messages:
            message_data = {
                'sender_id': message.sender.id,
                'sender_username': message.sender.username,
                'sender_first_name': message.sender.first_name,
                'sender_last_name': message.sender.last_name,
                'sender_profile_pic': message.sender.profile.image.url if message.sender.profile.image else '',
                'receiver_id': message.receiver.id,
                'receiver_username': message.receiver.username,
                'message': message.message,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            messages_data.append(message_data)
        
        return JsonResponse(messages_data, safe=False)

    elif request.method == 'POST':
        # Handling chat clearing
        user_id = user_pk

        logger.debug(f"clear_chat called with userId: {user_id}, roomId: {room_id}")

        try:
            chat_room = get_object_or_404(ChatRoom, users__id=user_id, id=room_id)
            
            # Check if the user is a participant in the chat room
            if request.user in chat_room.users.all():
                chat_room.messages.all().delete()
                logger.debug("Chat messages deleted successfully")
                return JsonResponse({'status': 'chat cleared'})
            else:
                logger.warning("Permission denied")
                return JsonResponse({'error': 'Permission denied'}, status=403)

        except ChatRoom.DoesNotExist:
            logger.error("Chat room not found")
            return JsonResponse({'error': 'Chat room not found'}, status=404)
        except Exception as e:
            logger.error(f"Error clearing chat: {e}")
            return JsonResponse({'error': 'An error occurred'}, status=500)

    else:
        # Handle other HTTP methods if needed
        logger.warning("Invalid HTTP method")
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)

@login_required
def chatPage(request, username):
    if not request.user.is_authenticated:
        return redirect("account_login")

    user_to_chat_with = None
    
    # Fetch the user to chat with based on username
    if username:
        try:
            user_to_chat_with = User.objects.get(username=username)
        except User.DoesNotExist:
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
            # Redirect back to the chat page after sending a message
            return redirect('chat_page', username=user_to_chat_with.username)

    chat_messages = ChatMessage.objects.filter(room=chat_room).order_by('-timestamp') if chat_room else None

    if request.GET.get('clear_chat'):
        if chat_room and request.user.has_perm('clear_chat', chat_room):
            chat_room.messages.all().delete()  # Assuming messages are related to the chat room

    # Fetch latest chat rooms for the current user
    user_chat_rooms = ChatRoom.objects.filter(users=request.user).order_by('-last_message_time')

    # Prepare user data for chat modal
    user_data = {
        'id': user_to_chat_with.pk,
        'username': user_to_chat_with.username,
        'email': user_to_chat_with.email,
        'company': user_to_chat_with.profile.company if hasattr(user_to_chat_with, 'profile') else '',
        'website': user_to_chat_with.profile.website if hasattr(user_to_chat_with, 'profile') else '',
        'location': user_to_chat_with.profile.location if hasattr(user_to_chat_with, 'profile') else '',
        'bio': user_to_chat_with.profile.bio if hasattr(user_to_chat_with, 'profile') else '',
        'githubusername': user_to_chat_with.profile.githubusername if hasattr(user_to_chat_with, 'profile') else '',
        'date': user_to_chat_with.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'image_url': user_to_chat_with.profile.image.url if hasattr(user_to_chat_with, 'profile') and user_to_chat_with.profile.image else '',
        'occupation': user_to_chat_with.profile.occupation if hasattr(user_to_chat_with, 'profile') else '',
        'skills': list(user_to_chat_with.profile.skills.values_list('name', flat=True)) if hasattr(user_to_chat_with, 'profile') else []
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
def fetch_chat_rooms(request):
    user_chat_rooms = ChatRoom.objects.filter(users=request.user).annotate(
        latest_message_time=Max('messages__timestamp')
    ).order_by('-latest_message_time')

    chat_rooms_data = []
    for room in user_chat_rooms:
        other_user = room.users.exclude(id=request.user.id).first()
        last_message = room.messages.order_by('-timestamp').first()
        if other_user:
            chat_rooms_data.append({
                'id': room.id,
                'other_user_id':other_user.id,
                'other_user_username': other_user.username,
                'other_user_first_name': other_user.first_name,
                'other_user_last_name': other_user.last_name,
                'other_user_profile_pic': other_user.profile.image.url,
                'latest_message_time': room.latest_message_time,
                'last_message_text': last_message.message if last_message else "No messages yet",
                'last_message_time_formatted': last_message.timestamp.strftime("%b %d") if last_message else "No messages yet",
            })

    return JsonResponse({'chat_rooms_data': chat_rooms_data})


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
    