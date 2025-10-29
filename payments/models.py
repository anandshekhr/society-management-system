from django.db import models
from django.utils import timezone


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PAID = 'Paid', 'Paid'
    OVERDUE = 'Overdue', 'Overdue'
    CANCELLED = 'Cancelled', 'Cancelled'


class PaymentMethod(models.TextChoices):
    CASH = 'Cash', 'Cash'
    ONLINE = 'Online', 'Online'
    CHEQUE = 'Cheque', 'Cheque'
    UPI = 'UPI', 'UPI'


class MaintenancePayment(models.Model):
    owner = models.ForeignKey(
        'authentication.Owner',
        on_delete=models.CASCADE,
        related_name='maintenance_payments'
    )
    flat = models.ForeignKey(
        'flats.Flat',
        on_delete=models.CASCADE,
        related_name='maintenance_payments'
    )

    invoice_no = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()  # 1–12
    year = models.IntegerField()
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.ONLINE
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    remarks = models.TextField(blank=True, null=True)
    receipt_file = models.FileField(upload_to='maintenance_receipts/', blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('flat', 'month', 'year')
        ordering = ['-year', '-month']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['month', 'year']),
        ]

    def __str__(self):
        return f"{self.flat.flat_no} - {self.month}/{self.year} - {self.status}"

class StaffPaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PAID = 'Paid', 'Paid'
    ON_HOLD = 'On Hold', 'On Hold'


class StaffPaymentMethod(models.TextChoices):
    CASH = 'Cash', 'Cash'
    BANK_TRANSFER = 'Bank Transfer', 'Bank Transfer'
    UPI = 'UPI', 'UPI'
    CHEQUE = 'Cheque', 'Cheque'


class StaffPayment(models.Model):
    employee = models.ForeignKey(
        'staff.Staff',
        on_delete=models.CASCADE,
        related_name='staff_payments'
    )
    society = models.ForeignKey(
        'society.Society',
        on_delete=models.CASCADE,
        related_name='staff_payments'
    )

    payment_month = models.IntegerField()
    payment_year = models.IntegerField()
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(
        max_length=20,
        choices=StaffPaymentMethod.choices,
        default=StaffPaymentMethod.BANK_TRANSFER
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=StaffPaymentStatus.choices,
        default=StaffPaymentStatus.PENDING
    )
    remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'payment_month', 'payment_year')
        ordering = ['-payment_year', '-payment_month']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['payment_month', 'payment_year']),
        ]

    def __str__(self):
        return f"{self.employee.name} - {self.payment_month}/{self.payment_year} - {self.status}"
