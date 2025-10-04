from django.db import models
from django.conf import settings
from campus.models import Campus

# Choices
GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
]

MARITAL_STATUS_CHOICES = [
    ("single", "Single"),
    ("married", "Married"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
]

SAVE_STATUS_CHOICES = [
    ("draft", "Draft"),
    ("final", "Final"),
]


class Principal(models.Model):
    # Basic Info
    full_name = models.CharField(max_length=150)
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    cnic = models.CharField(max_length=15, unique=True, blank=True, null=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, blank=True, null=True)

    # User link (auth)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="principal_profile",
        null=True, blank=True
    )

    # Campus Assignment
    campus = models.OneToOneField(
        Campus,
        on_delete=models.CASCADE,
        related_name="principal"
    )

    # Education Info
    highest_qualification = models.CharField(max_length=200, blank=True, null=True)
    institution_name = models.CharField(max_length=200, blank=True, null=True)
    year_of_passing = models.IntegerField(blank=True, null=True)
    specialization_subjects = models.CharField(max_length=200, blank=True, null=True)
    grade_obtained = models.CharField(max_length=50, blank=True, null=True)

    # Work Experience
    previous_institution = models.CharField(max_length=200, blank=True, null=True)
    previous_position = models.CharField(max_length=150, blank=True, null=True)
    experience_from_date = models.DateField(blank=True, null=True)
    experience_to_date = models.DateField(blank=True, null=True)
    total_experience_years = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Metadata
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    save_status = models.CharField(max_length=10, choices=SAVE_STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - Principal of {self.campus.campus_name}"

    class Meta:
        verbose_name = "Principal"
        verbose_name_plural = "Principals"
        ordering = ['-created_at']
