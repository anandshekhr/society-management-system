from django.db import models
from django.utils import timezone
# Create your models here.
class NotificationType(models.TextChoices):
    NOTICE = 'Notice', 'Notice'
    MAINTENANCE_REQUEST = 'MaintenanceRequest', 'Maintenance Request'
    PAYMENT = 'Payment', 'Payment'
    GENERAL = 'General', 'General'


class NotificationStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SENT = 'Sent', 'Sent'
    FAILED = 'Failed', 'Failed'
    READ = 'Read', 'Read'


class Notification(models.Model):
    recipient_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    type = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.GENERAL
    )

    entity_id = models.PositiveIntegerField(null=True, blank=True)  # e.g. related notice or payment ID
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"To: {self.recipient_user.username} | {self.type} | {self.status}"
