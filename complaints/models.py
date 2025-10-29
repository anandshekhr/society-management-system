from django.db import models
from django.utils import timezone


class ComplaintCategory(models.TextChoices):
    MAINTENANCE = 'Maintenance', 'Maintenance Issue'
    STAFF_BEHAVIOR = 'StaffBehavior', 'Staff Behavior'
    CLEANLINESS = 'Cleanliness', 'Cleanliness'
    SECURITY = 'Security', 'Security'
    NOISE = 'Noise', 'Noise / Disturbance'
    OTHER = 'Other', 'Other'


class ComplaintStatus(models.TextChoices):
    RECEIVED = 'Received', 'Received'
    UNDER_REVIEW = 'UnderReview', 'Under Review'
    IN_PROGRESS = 'InProgress', 'In Progress'
    RESOLVED = 'Resolved', 'Resolved'
    REJECTED = 'Rejected', 'Rejected'
    CLOSED = 'Closed', 'Closed'


class Complaint(models.Model):
    society = models.ForeignKey(
        'society.Society',
        on_delete=models.CASCADE,
        related_name='complaints'
    )
    raised_by = models.ForeignKey(
        'authentication.Owner',
        on_delete=models.CASCADE,
        related_name='complaints_raised'
    )
    assigned_to = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='complaints_assigned'
    )
    linked_maintenance = models.ForeignKey(
        'maintenance.MaintenanceRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_complaints'
    )

    category = models.CharField(
        max_length=50,
        choices=ComplaintCategory.choices,
        default=ComplaintCategory.OTHER
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.RECEIVED
    )
    priority = models.CharField(
        max_length=10,
        choices=[
            ('Low', 'Low'),
            ('Medium', 'Medium'),
            ('High', 'High')
        ],
        default='Medium'
    )

    raised_on = models.DateTimeField(default=timezone.now)
    resolved_on = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='complaints/', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-raised_on']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Complaint #{self.id} - {self.subject} ({self.status})"

    def mark_resolved(self, notes: str = None):
        """Helper method to mark complaint as resolved."""
        self.status = ComplaintStatus.RESOLVED
        self.resolved_on = timezone.now()
        if notes:
            self.resolution_notes = notes
        self.save()
