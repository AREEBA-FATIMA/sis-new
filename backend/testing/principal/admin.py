from django.contrib import admin
from .models import Principal

@admin.register(Principal)
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ("user", "campus", "qualification", "experience_years", "is_active")
    search_fields = ("user__username", "user__first_name", "user__last_name", "campus__campus_name")
    list_filter = ("is_active", "campus")
