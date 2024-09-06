from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    def __str__(self):
        return self.username
    
class ChatSession(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.pk}"

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} on {self.timestamp}"

