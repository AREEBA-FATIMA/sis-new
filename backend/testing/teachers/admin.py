from django.contrib import admin
from .models import Teacher, TeacherEducation, TeacherExperience, TeacherRole

# Teacher Education Inline
class TeacherEducationInline(admin.StackedInline):
    model = TeacherEducation
    extra = 1   # ek extra empty form dikhega
    classes = ['collapse']  # optional: collapse/expand karne ka option

# Teacher Experience Inline
class TeacherExperienceInline(admin.StackedInline):
    model = TeacherExperience
    extra = 1
    classes = ['collapse']

# Teacher Role Inline
class TeacherRoleInline(admin.StackedInline):
    model = TeacherRole
    extra = 1
    classes = ['collapse']

# Main Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "gender", "save_status", "date_created")
    search_fields = ("full_name", "email")
    list_filter = ("gender", "marital_status", "save_status")

    inlines = [TeacherEducationInline, TeacherExperienceInline, TeacherRoleInline]
