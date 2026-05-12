# DocuChat/models.py
import uuid
from django.db import models

class ChatSession(models.Model):
    # Django's internal reference AND LangGraph's thread ID
    session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('DocuProcess', on_delete=models.CASCADE, related_name='chat_sessions')
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Replaced thread_id with session_id
        return f"Chat for {self.project.project_id} | Thread: {self.session_id}"
    

class ChatMessage(models.Model):

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user_message = models.TextField()
    assistant_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.session.session_id} | {self.created_at}"
