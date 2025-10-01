from django.contrib import admin
from .models import Coordinator


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "gender",
        "section",
        "campus",
        "is_active",
        "created_at",
    )
    list_filter = ("section", "campus", "is_active", "gender")
    search_fields = ("full_name", "email", "phone", "cnic")
    ordering = ("-created_at",)

    # ✅ ManyToMany heavy fields ko optimize
    autocomplete_fields = ("grades", "classes", "teachers", "students")

    # agar foreign key campus ya section bhi bohot bara dataset ho sakta hai
    # to unko bhi autocomplete me daal sakte ho
    # autocomplete_fields = ("campus", "section", "grades", "classes", "teachers", "students")
