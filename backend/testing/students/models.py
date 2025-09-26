from django.db import models
from django.utils import timezone


class Student(models.Model):
    # --- Personal Details ---
    photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)
    name = models.CharField(max_length=200)  # Only required
    gender = models.CharField(
        max_length=10,
        choices=(("male", "Male"), ("female", "Female")),
        null=True,
        blank=True
    )
    dob = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    mother_tongue = models.CharField(max_length=100, null=True, blank=True)

    # --- Contact Details ---
    emergency_contact = models.CharField(max_length=20, null=True, blank=True)
    primary_phone = models.CharField(max_length=20, null=True, blank=True)

    father_name = models.CharField(max_length=200, null=True, blank=True)
    father_cnic = models.CharField(max_length=20, null=True, blank=True)
    father_contact = models.CharField(max_length=20, null=True, blank=True)
    father_occupation = models.CharField(max_length=200, null=True, blank=True)

    secondary_phone = models.CharField(max_length=20, null=True, blank=True)
    guardian_name = models.CharField(max_length=200, null=True, blank=True)
    guardian_cnic = models.CharField(max_length=20, null=True, blank=True)
    guardian_occupation = models.CharField(max_length=200, null=True, blank=True)

    mother_name = models.CharField(max_length=200, null=True, blank=True)
    mother_cnic = models.CharField(max_length=20, null=True, blank=True)
    mother_status = models.CharField(
        max_length=20,
        choices=(("widowed", "Widowed"), ("divorced", "Divorced"), ("married", "Married")),
        null=True,
        blank=True
    )
    mother_contact = models.CharField(max_length=20, null=True, blank=True)
    mother_occupation = models.CharField(max_length=200, null=True, blank=True)

    zakat_status = models.CharField(
        max_length=20,
        choices=(("applicable", "Applicable"), ("not_applicable", "Not Applicable")),
        null=True,
        blank=True
    )

    address = models.TextField(null=True, blank=True)
    family_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    house_owned = models.BooleanField(default=False)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # --- Academic Details ---
    current_state = models.CharField(
        max_length=20,
        choices=(("active", "Active"), ("inactive", "Not Active")),
        default="active"
    )
    campus = models.ForeignKey("campus.Campus", on_delete=models.SET_NULL, null=True, blank=True)

    # ✅ Old direct connection (still kept for backward compatibility)
    classroom = models.ForeignKey(
        "classes.ClassRoom",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    reason_for_transfer = models.TextField(null=True, blank=True)
    to_year = models.CharField(max_length=20, null=True, blank=True)
    from_year = models.CharField(max_length=20, null=True, blank=True)
    last_class_passed = models.CharField(max_length=50, null=True, blank=True)
    last_school_name = models.CharField(max_length=200, null=True, blank=True)
    old_gr_no = models.CharField(max_length=50, null=True, blank=True)

    gr_no = models.CharField(max_length=50, null=True, blank=True, unique=False)

    # --- System Fields ---
    is_draft = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.gr_no or 'No GR'})"


class StudentEnrollment(models.Model):
    """
    Ye model student ko specific classroom aur academic year se link karega.
    """
    student = models.ForeignKey(Student, related_name="enrollments", on_delete=models.CASCADE)
    classroom = models.ForeignKey("classes.ClassRoom", related_name="enrollments", on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=9, help_text="e.g. 2025-2026")
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "classroom", "academic_year")

    def __str__(self):
        return f"{self.student.name} → {self.classroom} ({self.academic_year})"
