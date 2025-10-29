from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Society
from authentication.models import Owner
from maintenance.models import MaintenanceRequest
from complaints.models import Complaint
from society_events.models import Event
from notice.models import Notice
from notification.models import Notification
from staff.models import StaffAttendance, Staff
from entry_exit.models import InOutRecord
from payments.models import MaintenancePayment, StaffPayment


@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at')

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ( 'flat', 'phone')
    search_fields = ( 'flat',)

@admin.register(Staff)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'contact_phone', 'status')
    list_filter = ('role', 'status')

# @admin.register(MaintenanceRequest.MaintenanceCategory)
# class MaintenanceCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'owner', 'assigned_employee')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'status', 'raised_by', 'assigned_to')
    list_filter = ('status', 'category')
    search_fields = ('subject', 'description')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'start_datetime', 'venue')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'priority', 'posted_on', 'is_active')
    list_filter = ('audience', 'priority')
    search_fields = ('title', 'message')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient_user', 'type', 'status', 'sent_at')
    list_filter = ('type', 'status')
    search_fields = ('subject', 'message')

@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'check_in', 'check_out')
    list_filter = ('status', 'date')
    search_fields = ('employee__name',)

@admin.register(InOutRecord)
class InOutRecordAdmin(admin.ModelAdmin):
    list_display = ('person_type', 'employee', 'visitor_name', 'entry_type', 'timestamp', 'gate_number')
    list_filter = ('person_type', 'entry_type')
    search_fields = ('employee__name', 'visitor_name')

@admin.register(MaintenancePayment)
class MaintenancePaymentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'status', 'payment_date')
    list_filter = ('status',)
    search_fields = ('owner__user__username',)

@admin.register(StaffPayment)
class StaffPaymentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary_amount', 'payment_month', 'status')
    list_filter = ('status', 'payment_month')
    search_fields = ('employee__name',)
