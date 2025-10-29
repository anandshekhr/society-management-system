from django.db import models
from django.utils import timezone


class EntryType(models.TextChoices):
    IN = 'IN', 'Check-In'
    OUT = 'OUT', 'Check-Out'


class PersonType(models.TextChoices):
    EMPLOYEE = 'Employee', 'Employee'
    VISITOR = 'Visitor', 'Visitor'
    DELIVERY = 'Delivery', 'Delivery'


class InOutRecord(models.Model):
    society = models.ForeignKey(
        'society.Society',
        on_delete=models.CASCADE,
        related_name='inout_records'
    )

    person_type = models.CharField(
        max_length=20,
        choices=PersonType.choices,
        default=PersonType.EMPLOYEE
    )

    employee = models.ForeignKey(
        'staff.Staff',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='inout_records'
    )

    visitor_name = models.CharField(max_length=100, null=True, blank=True)
    visitor_contact = models.CharField(max_length=15, null=True, blank=True)
    visitor_purpose = models.CharField(max_length=255, null=True, blank=True)

    entry_type = models.CharField(
        max_length=10,
        choices=EntryType.choices
    )

    timestamp = models.DateTimeField(default=timezone.now)
    gate_number = models.CharField(max_length=50, null=True, blank=True)
    verified_by = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_entries'
    )

    remarks = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['entry_type']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['person_type']),
        ]

    def __str__(self):
        who = self.employee.name if self.employee else self.visitor_name
        return f"{who} - {self.entry_type} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
