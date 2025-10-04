from django.contrib import admin
from .models import Principal

@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "campus", "highest_qualification", "total_experience_years", "is_active")
    search_fields = ("full_name", "email", "campus__campus_name")
    list_filter = ("is_active", "campus")
