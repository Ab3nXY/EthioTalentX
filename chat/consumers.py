import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage  # Import your chat app models
from asgiref.sync import sync_to_async  # Import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        self.user = None

        # Get user from request (assuming authentication is set up)
        # Replace this with your authentication logic
        user_id = self.scope['user'].pk  # This might need adjustment based on your setup
        self.user = await sync_to_async(User.objects.get)(pk=user_id)

        # Check for room name in query string (optional)
        room_name_query = self.scope['query_string'].decode()
        if room_name_query:
            room_name_parts = room_name_query.split('=')
            if len(room_name_parts) == 2 and room_name_parts[0] == 'room':
                self.room_name = room_name_parts[1]

        # If room name is not provided, handle it appropriately
        if not self.room_name:
            new_room_name = f"chat_{self.user.username}"  # Example: chat_user1
            new_room, created = await sync_to_async(ChatRoom.objects.get_or_create)(name=new_room_name)
            self.room_name = new_room.name
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the room group
        if self.room_name:
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        room_id = text_data_json["room_id"]  # Access the room ID

        # Check if room_id is valid and user is authenticated (adjust logic)
        if not room_id or not self.user:
            return

        try:
            chat_room = await sync_to_async(ChatRoom.objects.get)(pk=room_id)  # Get the chat room
        except ChatRoom.DoesNotExist:
            # Handle invalid room ID
            return

        # Check if user is authenticated and in a room
        if not self.user or not self.room_name:
            return

        # Create and save the chat message
        chat_message = await sync_to_async(ChatMessage.objects.create)(
            sender=self.user,
            room=await sync_to_async(ChatRoom.objects.get)(name=self.room_name),  # Assuming room has a name field
            message=message
        )

        # Broadcast the message to the room
        await self.channel_layer.group_send(
            self.room_name, {
                "type": "send_message",
                "message": chat_message.message,
                "username": self.user.username,
            }
        )

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        room_id = event["room_id"]  # Access the room ID

        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))
