from django.contrib import admin
from .models import AttendanceType, AttendanceRegister, AttendanceSheet, AttendanceLine


@admin.register(AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "present", "excused", "absent", "late", "active")
    list_filter = ("active", "present", "excused", "absent", "late")
    search_fields = ("name",)


@admin.register(AttendanceRegister)
class AttendanceRegisterAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "course", "batch", "subject", "active")
    list_filter = ("course", "batch", "active")
    search_fields = ("name", "code")


@admin.register(AttendanceSheet)
class AttendanceSheetAdmin(admin.ModelAdmin):
    list_display = ("register", "course", "batch", "session", "attendance_date", "faculty", "state", "active")
    list_filter = ("course", "batch", "state", "attendance_date")
    search_fields = ("register__code", "faculty__name")
    date_hierarchy = "attendance_date"


@admin.register(AttendanceLine)
class AttendanceLineAdmin(admin.ModelAdmin):
    list_display = ("attendance_sheet", "student", "present", "excused", "absent", "late", "attendance_date", "remark")
    list_filter = ("present", "excused", "absent", "late", "attendance_date")
    search_fields = ("student__name", "attendance_sheet__register__code", "remark")
