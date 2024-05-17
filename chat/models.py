from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, default="")
    users = models.ManyToManyField(User, related_name='chatrooms')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat Room ({', '.join(str(user) for user in self.users.all())})"

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', default='')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Message (From: {self.sender}, To: {self.receiver}, Room: {self.room.id}, Message: {self.message[:20]}...)"
