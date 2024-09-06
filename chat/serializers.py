from rest_framework import serializers
from .models import User, Message, ChatSession
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timesince import timesince

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class ChatSessionSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    class Meta:
        model = ChatSession
        fields = ['id', 'created_at', 'participants', 'last_message']

    def get_last_message(self, obj):
        last_message = obj.messages.order_by('-timestamp').first()  # Get the most recent message
        if last_message:
            time_since = timesince(last_message.timestamp).split(',')[0]  # Simplify to the most significant unit
            if last_message.sender == self.context['request'].user:
                return {"message": f"You: {last_message.content}", "timestamp": time_since, "exact_time": last_message.timestamp.isoformat(), "read": last_message.read, "id": last_message.id, "sender": "user"}
            else:
                return {"message": last_message.content, "timestamp": time_since, "exact_time": last_message.timestamp.isoformat(), "read": last_message.read, "id": last_message.id, "sender": "other_user"}
        return None