# attendance/models.py
from django.db import models

class AttendanceSheet(models.Model):
    campus = models.ForeignKey("campus.Campus", on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.class_name} - {self.month}/{self.year}"


class AttendanceRecord(models.Model):
    sheet = models.ForeignKey(AttendanceSheet, on_delete=models.CASCADE, related_name="records")
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=1,
        choices=[
            ("P", "Present"),
            ("L", "Late"),
            ("E", "Excused"),
            ("U", "Unexcused"),
        ],
        default="P",
    )
    marked_by = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ("student", "date", "sheet")  # ek din ek student ki ek hi entry

    def __str__(self):
        return f"{self.student} - {self.date} ({self.status})"
