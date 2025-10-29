from django.db import models
from django.utils import timezone


class NoticeAudience(models.TextChoices):
    ALL = 'All', 'All'
    OWNERS = 'Owners', 'Owners'
    EMPLOYEES = 'Employees', 'Employees'


class NoticePriority(models.TextChoices):
    LOW = 'Low', 'Low'
    NORMAL = 'Normal', 'Normal'
    HIGH = 'High', 'High'
    URGENT = 'Urgent', 'Urgent'


class Notice(models.Model):
    society = models.ForeignKey(
        'society.Society',
        on_delete=models.CASCADE,
        related_name='notices'
    )
    posted_by = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posted_notices'
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    audience = models.CharField(
        max_length=20,
        choices=NoticeAudience.choices,
        default=NoticeAudience.ALL
    )
    priority = models.CharField(
        max_length=20,
        choices=NoticePriority.choices,
        default=NoticePriority.NORMAL
    )
    posted_on = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    attachment = models.FileField(upload_to='notice_attachments/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-posted_on']
        indexes = [
            models.Index(fields=['priority']),
            models.Index(fields=['audience']),
        ]

    def __str__(self):
        return f"{self.title} ({self.audience})"

    def is_expired(self):
        return self.expiry_date and self.expiry_date < timezone.now().date()
