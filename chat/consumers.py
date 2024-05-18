import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        self.user = None

        if self.scope['user'].is_authenticated:
            user_id = self.scope['user'].pk
            self.user = await sync_to_async(User.objects.get)(pk=user_id)

            room_name_query = self.scope['query_string'].decode()
            if room_name_query:
                room_name_parts = room_name_query.split('=')
                if len(room_name_parts) == 2 and room_name_parts[0] == 'room':
                    self.room_name = room_name_parts[1]

            if not self.room_name:
                self.room_name = f"chat_{self.user.pk}"

            await self.channel_layer.group_add(
                self.room_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.room_name:
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        receiver_id = text_data_json.get("receiver_id")
        room_id = text_data_json.get("roomId")
        print("Chat room = ", room_id)

        if message and receiver_id and room_id:
            try:
                sender = self.user
                receiver = await sync_to_async(User.objects.get)(pk=receiver_id)
                room = await sync_to_async(ChatRoom.objects.get)(pk=room_id)
                print(f"Receiver: {receiver.username}, Room: {room.name}")

                # Save message to database
                chat_message = await sync_to_async(ChatMessage.objects.create)(
                    sender=self.user,
                    receiver=receiver,
                    room=room,
                    message=message
                )

                # Broadcast message to room group
                await self.channel_layer.group_send(
                    self.room_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': sender.id,
                        'sender_username': sender.username,
                        'receiver_id': receiver.id,
                        'receiver_username': receiver.username,
                        'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    }
                )

            except User.DoesNotExist:
                print("Receiver user does not exist")
                return
            except ChatRoom.DoesNotExist:
                print("Chat room does not exist")
                return

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        receiver_id = event['receiver_id']
        receiver_username = event['receiver_username']
        timestamp = event['timestamp']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
            'sender_username': sender_username,
            'receiver_id': receiver_id,
            'receiver_username': receiver_username,
            'timestamp': timestamp
        }))
