from django.contrib import admin
from .models import Student, StudentEnrollment
from principal.models import Principal
from coordinator.models import Coordinator


class PrincipalFilter(admin.SimpleListFilter):
    title = "Principal"
    parameter_name = "principal"

    def lookups(self, request, model_admin):
        principals = Principal.objects.all()
        return [(p.id, f"{p.user.get_full_name()} - {p.campus.campus_name}") for p in principals]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(campus__principal__id=self.value())
        return queryset


class CoordinatorFilter(admin.SimpleListFilter):
    title = "Coordinator"
    parameter_name = "coordinator"

    def lookups(self, request, model_admin):
        coordinators = Coordinator.objects.all()
        return [(c.id, f"{c.full_name} - {c.campus.campus_name}") for c in coordinators]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(coordinator__id=self.value())
        return queryset


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "student_code",
        "gr_no",
        "classroom",
        "campus",
        "shift",
        "enrollment_year",
        "current_state",
    )
    list_filter = (
        "campus",
        "shift",
        "enrollment_year",
        "current_state",
        PrincipalFilter,   # 👈 Principal filter
        CoordinatorFilter, # 👈 Coordinator filter
    )
    search_fields = ("name", "student_code", "gr_no")


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "classroom", "academic_year", "date_enrolled")
    list_filter = ("academic_year", "classroom")
    search_fields = ("student__name", "classroom__grade__name")
