from django.contrib import admin
from .models import Student, StudentEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "student_code",   # 👈 Student Code added here
        "gr_no",
        "classroom",
        "campus",
        "shift",
        "enrollment_year",
        "current_state",
    )
    list_filter = ("campus", "shift", "enrollment_year", "current_state")
    search_fields = ("name", "student_code", "gr_no")


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "academic_year", "date_enrolled")
    list_filter = ("academic_year", "classroom")
    search_fields = ("student__name", "classroom__grade__name")
