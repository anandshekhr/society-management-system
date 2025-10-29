from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from society.models import Society
from django.utils import timezone


class Staff(models.Model):
    class StaffRole(models.TextChoices):
        # Core Facility Roles
        SECURITY = "SEC", _("Security")
        CLEANING = "CLN", _("Cleaning")
        MAINTENANCE = "MNT", _("Maintenance")
        ELECTRICAL = "ELC", _("Electrical")
        PLUMBING = "PLB", _("Plumbing")
        GARDENING = "GRD", _("Gardening")
        HOUSEKEEPING = "HSK", _("Housekeeping")
        MAID = "MID", _("Maid")

        # Administrative / Support Roles
        ADMINISTRATIVE = "ADM", _("Administrative")
        RECEPTIONIST = "RCP", _("Receptionist")
        OFFICE_ASSISTANT = "OAS", _("Office Assistant")
        SUPERVISOR = "SUP", _("Supervisor")
        MANAGER = "MGR", _("Manager")

        # Technical / IT Roles
        IT_SUPPORT = "ITS", _("IT Support")
        NETWORK_ENGINEER = "NET", _("Network Engineer")
        TECHNICIAN = "TEC", _("Technician")

        # Logistics / Operations
        DRIVER = "DRV", _("Driver")
        STOREKEEPER = "STK", _("Storekeeper")
        DISPATCH = "DSP", _("Dispatch")
        COURIER = "COU", _("Courier")

        # Hospitality / Services
        CHEF = "CHF", _("Chef")
        COOK = "COK", _("Cook")
        WAITER = "WTR", _("Waiter")
        LAUNDRY = "LDR", _("Laundry")
        CATERING = "CTR", _("Catering")

        # Medical / Emergency
        NURSE = "NRS", _("Nurse")
        FIRST_AID = "FAD", _("First Aid Staff")
        FIRE_SAFETY = "FSF", _("Fire Safety Officer")

        # Miscellaneous
        WATCHMAN = "WTM", _("Watchman")
        LIFT_OPERATOR = "LTO", _("Lift Operator")
        ELECTRICIAN = "ELE", _("Electrician")
        CARPENTER = "CAR", _("Carpenter")
        PAINTER = "PNT", _("Painter")
    society = models.ForeignKey(Society, verbose_name=_("Society"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=255)
    role = models.CharField(_("Role"), max_length=255, choices=StaffRole.choices, default=StaffRole.SECURITY)
    contact_email = models.EmailField(_("Contact Email"), blank=True, null=True)
    contact_phone = models.CharField(_("Contact Phone"), max_length=20, blank=True, null=True)
    status = models.IntegerField(_("Status"), max_length=50, choices=[(0, 'Active'), (1, 'Inactive')], default=0)
    hired_date = models.DateField(_("Hired Date"), blank=True, null=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Staff")
        verbose_name_plural = _("Staffs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Staff_detail", kwargs={"pk": self.pk})

class AttendanceStatus(models.TextChoices):
    PRESENT = 'Present', 'Present'
    ABSENT = 'Absent', 'Absent'
    LEAVE = 'Leave', 'Leave'
    HALF_DAY = 'Half Day', 'Half Day'


class StaffAttendance(models.Model):
    employee = models.ForeignKey(
        'staff.Staff',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT
    )
    remarks = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        'staff.Staff',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_marked_by'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.date} ({self.status})"
