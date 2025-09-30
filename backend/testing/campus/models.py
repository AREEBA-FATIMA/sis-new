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
        unique=True,
        editable=False,
        help_text="Auto-generated: CITY-YEAR-POSTAL-NO (e.g., KHI-16-75080-01)"
    )
    campus_code = models.CharField(max_length=50, unique=True)
    # code = models.CharField(max_length=10, unique=True, editable=False, help_text="Short code for references")
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

    def save(self, *args, **kwargs):
        # Auto-generate campus_id if not provided
        if not self.campus_id:
            city_code = self.city[:3].upper() if self.city else "CMP"
            year_code = str(self.established_year or 2025)[-2:]
            postal_code = self.postal_code[-5:] if self.postal_code else "00000"
            
            # Get next number for this city-year combination
            last_campus = Campus.objects.filter(
                campus_id__startswith=f"{city_code}-{year_code}-{postal_code}"
            ).order_by("-id").first()
            
            if last_campus and last_campus.campus_id:
                try:
                    last_num = int(last_campus.campus_id.split("-")[-1])
                except:
                    last_num = 0
            else:
                last_num = 0
            
            self.campus_id = f"{city_code}-{year_code}-{postal_code}-{(last_num + 1):02d}"
        
        # Auto-generate short code if not provided
        # if not self.code:
        #     # Create short code from campus name
        #     name_words = self.campus_name.split()
        #     if len(name_words) >= 2:
        #         self.code = f"{name_words[0][:2]}{name_words[1][:2]}".upper()
        #     else:
        #         self.code = self.campus_name[:4].upper()
        #     
        #     # Ensure uniqueness
        #     original_code = self.code
        #     counter = 1
        #     while Campus.objects.filter(code=self.code).exclude(pk=self.pk).exists():
        #         self.code = f"{original_code}{counter}"
        #         counter += 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.campus_name} ({self.campus_code})"
