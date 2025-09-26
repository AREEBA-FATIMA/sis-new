from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "gr_no",
        "get_class_teacher",   # ✅ Show teacher name (from classroom)
        "classroom",
        "campus",
        "current_state",
    )
    list_filter = (
        "current_state",
        "campus",
        "classroom__grade",
        "classroom__section",
        "classroom__class_teacher",  # ✅ Filter by class teacher
    )
    search_fields = ("name", "gr_no")

    @admin.display(ordering="classroom__class_teacher", description="Class Teacher")
    def get_class_teacher(self, obj):
        if obj.classroom and obj.classroom.class_teacher:
            return str(obj.classroom.class_teacher)   # ✅ uses Teacher.__str__
        return "-"
