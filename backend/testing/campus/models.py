from django.db import models

class Campus(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("closed", "Closed"),
        ("under_construction", "Under Construction"),
    ]

    CAMPUS_TYPE_CHOICES = [
        ("main", "Main"),
        ("branch", "Branch"),
    ]

    SHIFT_CHOICES = [
        ("morning", "Morning"),
        ("afternoon", "Afternoon"),
        ("both", "Both"),
    ]

    # 🔹 Basic Info
    campus_id = models.CharField(
        max_length=50,
        help_text="Format: CITY-YEAR-POSTAL-NO (e.g., KHI-16-75080-01)"
    )
    campus_code = models.CharField(max_length=50)
    campus_name = models.CharField(max_length=255)
    campus_type = models.CharField(max_length=20, choices=CAMPUS_TYPE_CHOICES, default="main")
    governing_body = models.CharField(max_length=255, blank=True, null=True)
    accreditation = models.CharField(max_length=255, blank=True, null=True)
    languages_of_instruction = models.CharField(max_length=255, help_text="e.g. English, Urdu")
    academic_year_start = models.DateField()
    academic_year_end = models.DateField()

    # 🔹 Location Details
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    province_state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="Pakistan")
    postal_code = models.CharField(max_length=20)

    # 🔹 Contact Details
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    official_email = models.EmailField()

    # 🔹 Administration
    head_name = models.CharField(max_length=255, help_text="Principal / Director name")
    head_contact = models.CharField(max_length=100, blank=True, null=True)
    head_coordinator_name = models.CharField(max_length=255, blank=True, null=True)
    head_coordinator_contact = models.CharField(max_length=100, blank=True, null=True)
    total_staff_members = models.PositiveIntegerField(default=0)
    total_teachers = models.PositiveIntegerField(default=0)
    total_coordinators = models.PositiveIntegerField(default=0)
    total_maids = models.PositiveIntegerField(default=0)
    total_guards = models.PositiveIntegerField(default=0)
    other_staff = models.PositiveIntegerField(default=0)

    # 🔹 Operational Info
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    shift_available = models.CharField(max_length=20, choices=SHIFT_CHOICES, default="morning")
    education_levels = models.TextField(
        blank=True,
        help_text="Comma-separated education levels e.g. Primary, Secondary, College, IT Courses"
    )
    student_capacity = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # 🔹 Infrastructure
    num_rooms = models.PositiveIntegerField(default=0)
    total_classrooms = models.PositiveIntegerField(default=0)
    avg_class_size = models.PositiveIntegerField(default=0)
    current_class_size = models.PositiveIntegerField(default=0)
    num_computer_labs = models.PositiveIntegerField(default=0)
    num_science_labs = models.PositiveIntegerField(default=0)
    num_language_labs = models.PositiveIntegerField(default=0)
    library_available = models.BooleanField(default=False)
    sports_facilities = models.BooleanField(default=False)
    transport_facility = models.BooleanField(default=False)
    canteen_available = models.BooleanField(default=False)
    meals_available = models.BooleanField(default=False)
    num_toilets = models.PositiveIntegerField(default=0)
    toilets_male = models.PositiveIntegerField(default=0)
    toilets_female = models.PositiveIntegerField(default=0)
    toilets_accessible = models.PositiveIntegerField(default=0)
    toilets_teachers = models.PositiveIntegerField(default=0)
    facilities = models.TextField(blank=True, null=True)
    other_facilities = models.TextField(
        blank=True,
        null=True,
        help_text="Extra facilities in plain text (comma separated or free text)"
    )
    power_backup = models.BooleanField(default=False)
    internet_wifi = models.BooleanField(default=False)

    # 🔹 Draft system
    is_draft = models.BooleanField(default=True)

    # 🔹 System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.campus_name} ({self.campus_code})"
