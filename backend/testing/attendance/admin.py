from django.contrib import admin
from .models import AttendanceSheet, AttendanceRecord

@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ("class_name", "campus", "month", "year", "created_at")

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ("sheet", "student", "date", "status", "marked_by")
    list_filter = ("sheet__class_name", "date", "status")
    search_fields = ("student__name", "sheet__class_name")
