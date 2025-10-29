from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class MaintenanceRequest(models.Model):
    class MaintenanceCategory(models.TextChoices):
        ELECTRICAL = "ELC", _("Electrical")
        PLUMBING = "PLB", _("Plumbing")
        HVAC = "HVC", _("HVAC / Air Conditioning")
        CIVIL = "CIV", _("Civil / Structural")
        GARDENING = "GRD", _("Gardening")
        CLEANING = "CLN", _("Cleaning")
        PAINTING = "PNT", _("Painting")
        HOUSEKEEPING = "HSK", _("Housekeeping")
        PEST_CONTROL = "PST", _("Pest Control")
        LIFT = "LFT", _("Lift / Elevator")
        FIRE_SAFETY = "FSF", _("Fire Safety")
        GENERAL = "GEN", _("General Maintenance")


    class MaintenanceStatus(models.TextChoices):
        PENDING = "PND", _("Pending")
        IN_PROGRESS = "INP", _("In Progress")
        COMPLETED = "CMP", _("Completed")
        ON_HOLD = "HLD", _("On Hold")
        CANCELLED = "CNL", _("Cancelled")

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Urgent', 'Urgent'),
    ]

    owner = models.ForeignKey(
        'authentication.Owner',
        on_delete=models.CASCADE,
        related_name='maintenance_requests'
    )

    category = models.CharField(_("Maintenance Category"), max_length=50, choices=MaintenanceCategory.choices, default=MaintenanceCategory.GENERAL)

    assigned_employee = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests'
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=MaintenanceStatus.choices, default=MaintenanceStatus.PENDING)
    attachment = models.FileField(upload_to='maintenance_attachments/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.status}) - {self.owner.user.username}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
