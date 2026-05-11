from django.db import models
from django.conf import settings


class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    # NOTE: NOT auto_now so we can manually bump it on new message
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation #{self.id}"

    def get_other_participant(self, user):
        return self.participants.exclude(id=user.id).first()

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    MSG_TYPES = [
        ('text',      'Text'),
        ('voice',     'Voice'),
        ('image',     'Image'),
        ('job_share', 'Job Share'),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_type = models.CharField(max_length=20, choices=MSG_TYPES, default='text')
    content      = models.TextField(blank=True)
    voice_file   = models.FileField(upload_to='voice_messages/', blank=True, null=True)
    image_file   = models.ImageField(upload_to='message_images/', blank=True, null=True)
    is_read      = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg from {self.sender.username}: {self.content[:40]}"
