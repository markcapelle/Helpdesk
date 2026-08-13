from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conv_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conv_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    def participants(self):
        return [self.user1, self.user2]

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen_by = models.ManyToManyField(User, related_name="seen_messages", blank=True)


    def __str__(self):
        return f"Msg {self.id} in Conv {self.conversation.id}"
