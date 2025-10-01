from django.db import models
from campus.models import Campus
from classes.models import Grade, ClassRoom
from students.models import Student
from teachers.models import Teacher


class Coordinator(models.Model):
    """
    Coordinator model: Responsible for a group of classes, teachers, and students.
    Example: Primary Section Coordinator (Grade 1–5)
    """

    SECTION_CHOICES = [
        ("pre_primary", "Pre-Primary"),
        ("primary", "Primary"),
        ("secondary", "Secondary"),
    ]

    # Basic Info
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    cnic = models.CharField(max_length=15, unique=True)

    # Work Assignment
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name="coordinators")
    section = models.CharField(max_length=20, choices=SECTION_CHOICES, default="primary")
    
    # Coordinator handles multiple grades (e.g. Grade 1–5 for Primary)
    grades = models.ManyToManyField(Grade, related_name="coordinators")

    # Coordinator can directly assign classes
    classes = models.ManyToManyField(ClassRoom, related_name="coordinators", blank=True)

    # Teachers under this coordinator
    teachers = models.ManyToManyField(Teacher, related_name="coordinators", blank=True)

    # Students under this coordinator (optional, can be auto-linked via classes)
    students = models.ManyToManyField(Student, related_name="coordinators", blank=True)

    # Metadata
    date_joined = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.section} ({self.campus.campus_name})"
