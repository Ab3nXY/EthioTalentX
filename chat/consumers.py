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
        if self.scope['user'].is_authenticated:
            user_id = self.scope['user'].pk
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

            # Add user to the room group
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
        message = text_data_json.get("message")
        username = text_data_json.get("username")
        receiver_id = text_data_json.get("receiver_id")  # Access the receiver userPk
        room_id = text_data_json.get("room_id")  # Access the room ID

        # Check if message, username, receiver_id, and room_id are present
        if message and username and receiver_id and room_id:
            try:
                receiver = await sync_to_async(User.objects.get)(pk=receiver_id)  # Get the receiver user
            except User.DoesNotExist:
                # Handle invalid receiver ID
                return

            # Create and save the chat message with the receiver and room
            chat_message = await sync_to_async(ChatMessage.objects.create)(
                sender=self.user,
                receiver=receiver,
                room_id=room_id,
                message=message
            )

            # Broadcast the message to the room
            await self.channel_layer.group_send(
                self.room_name, {
                    "type": "send_message",
                    "message": chat_message.message,
                    "username": username,
                }
            )


    async def send_message(self, event):
        message = event["message"]
        username = event["username"]

        data = {
            "message": message,
            "username": username,
        }
        print("Sending data:", data)  # Log the data before sending
        await self.send(text_data=json.dumps(data))
