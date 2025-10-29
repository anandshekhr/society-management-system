from django.db import models
from django.utils import timezone


# Create your models here.
class EventCategory(models.TextChoices):
    FESTIVAL = 'Festival', 'Festival Celebration'
    MEETING = 'Meeting', 'Committee Meeting'
    SPORTS = 'Sports', 'Sports / Competition'
    CULTURAL = 'Cultural', 'Cultural Program'
    CLEANUP = 'Cleanup', 'Clean-up Drive'
    OTHER = 'Other', 'Other'


class EventStatus(models.TextChoices):
    UPCOMING = 'Upcoming', 'Upcoming'
    ONGOING = 'Ongoing', 'Ongoing'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'


class Event(models.Model):
    society = models.ForeignKey(
        'society.Society',
        on_delete=models.CASCADE,
        related_name='events'
    )
    created_by = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events_created'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=30,
        choices=EventCategory.choices,
        default=EventCategory.OTHER
    )
    status = models.CharField(
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.UPCOMING
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    venue = models.CharField(max_length=255)
    organized_by = models.CharField(max_length=255, null=True, blank=True)
    participants = models.ManyToManyField(
        'authentication.Owner',
        blank=True,
        related_name='events_participating'
    )

    cover_image = models.ImageField(upload_to='events/covers/', null=True, blank=True)
    banner = models.ImageField(upload_to='events/banners/', null=True, blank=True)
    is_public = models.BooleanField(default=True)
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"

    def is_active(self):
        return self.start_datetime <= timezone.now() <= self.end_datetime
