from django.db import models


# Create your models here.
class Mails(models.Model):
    mail_id = models.CharField(max_length=100)
    thread_id = models.CharField(max_length=100)
    message_body = models.CharField(max_length=10000)
    sender = models.CharField(max_length=100)
    mail_datetime = models.DateTimeField(null=True, blank=True)
    subject = models.CharField(max_length=100)
    read_status = models.BooleanField(default=False)
    mail_tag = models.CharField(max_length=100, default='INBOX')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "Mails"

        indexes = [
            models.Index(fields=['thread_id'])
        ]
