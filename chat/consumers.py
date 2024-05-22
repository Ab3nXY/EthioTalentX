import json
import logging
from django.contrib.auth.models import User
from accounts.models import Profile
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from asgiref.sync import sync_to_async

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        self.user = None

        if self.scope['user'].is_authenticated:
            user_id = self.scope['user'].pk
            self.user = await sync_to_async(User.objects.get)(pk=user_id)

            query_string = self.scope['query_string'].decode()
            room_name_query = query_string.split('&')
            for param in room_name_query:
                key, value = param.split('=')
                if key == 'room':
                    self.room_name = value
                    break

            if not self.room_name:
                await self.close()
                return

            logger.info(f"User {self.user.username} (ID: {self.user.pk}) is connecting to room: {self.room_name}")

            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.room_name:
            logger.info(f"User {self.user.username} (ID: {self.user.pk}) is disconnecting from room: {self.room_name}")
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        receiver_id = text_data_json.get("receiver_id")
        room_id = text_data_json.get("roomId")

        if message and receiver_id and room_id:
            try:
                sender = self.user
                profile = await sync_to_async(lambda: sender.profile)()
                sender_profile_image_url = profile.image.url
                receiver = await sync_to_async(User.objects.get)(pk=receiver_id)
                room = await sync_to_async(ChatRoom.objects.get)(pk=room_id)

                chat_message = await sync_to_async(ChatMessage.objects.create)(
                    sender=self.user,
                    receiver=receiver,
                    room=room,
                    message=message
                )

                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': sender.id,
                        'sender_username': sender.username,
                        'sender_profile_image_url': sender_profile_image_url,
                        'sender_first_name': sender.first_name,
                        'sender_last_name': sender.last_name,
                        'receiver_id': receiver.id,
                        'receiver_username': receiver.username,
                        'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    }
                )

            except User.DoesNotExist:
                logger.error(f"Receiver with ID {receiver_id} does not exist")
                return
            except ChatRoom.DoesNotExist:
                logger.error(f"Chat room with ID {room_id} does not exist")
                return

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        sender_first_name = event['sender_first_name']
        sender_last_name = event['sender_last_name']
        sender_profile_image_url = event['sender_profile_image_url']
        receiver_id = event['receiver_id']
        receiver_username = event['receiver_username']
        timestamp = event['timestamp']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username,
            'sender_proile_picture': sender_profile_image_url,
            'sender_first_name': sender_first_name,
            'sender_last_name': sender_last_name,
            'receiver_id': receiver_id,
            'receiver_username': receiver_username,
            'timestamp': timestamp
        }))
