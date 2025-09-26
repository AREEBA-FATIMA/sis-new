from django.db import models
from django.utils import timezone


# -----------------------------
# Attendance Type
# -----------------------------
class AttendanceType(models.Model):
    name = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    present = models.BooleanField(default=False)
    excused = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    late = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# -----------------------------
# Attendance Register
# -----------------------------
class AttendanceRegister(models.Model):
    name = models.CharField(max_length=16)
    code = models.CharField(max_length=16, unique=True)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    batch = models.ForeignKey(
        "courses.Batch",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    subject = models.ForeignKey(
        "courses.Subject",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# -----------------------------
# Attendance Sheet
# -----------------------------
class AttendanceSheet(models.Model):
    register = models.ForeignKey(
        AttendanceRegister,
        on_delete=models.CASCADE,
        related_name="sheets",
        null=True, blank=True
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    batch = models.ForeignKey(
        "courses.Batch",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    session = models.ForeignKey(
        "sessions.Session",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    attendance_date = models.DateField(default=timezone.now)
    faculty = models.ForeignKey(
        "faculty.Faculty",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    active = models.BooleanField(default=True)

    STATE_CHOICES = [
        ('draft', 'Draft'),
        ('start', 'Attendance Start'),
        ('done', 'Attendance Taken'),
        ('cancel', 'Cancelled'),
    ]
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='draft')

    class Meta:
        unique_together = ('register', 'session', 'attendance_date')

    def __str__(self):
        return f"{self.register.code if self.register else 'N/A'} - {self.attendance_date}"


# -----------------------------
# Attendance Line
# -----------------------------
class AttendanceLine(models.Model):
    attendance_sheet = models.ForeignKey(
        AttendanceSheet,
        on_delete=models.CASCADE,
        related_name="lines",
        null=True, blank=True
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    present = models.BooleanField(default=False)
    excused = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    late = models.BooleanField(default=False)
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    batch = models.ForeignKey(
        "courses.Batch",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    remark = models.CharField(max_length=256, blank=True, null=True)
    attendance_date = models.DateField(default=timezone.now)
    register = models.ForeignKey(
        AttendanceRegister,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    active = models.BooleanField(default=True)
    attendance_type = models.ForeignKey(
        AttendanceType,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        unique_together = ('student', 'attendance_sheet', 'attendance_date')

    def __str__(self):
        return f"{self.student} - {self.attendance_date}"
