from django.db import models

# ===================== Exam Model =====================
class Exam(models.Model):
    name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=20)
    campus = models.ForeignKey("campus.Campus", on_delete=models.CASCADE)  # Campus ab available hai

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


# ===================== ExamResult Model =====================
class ExamResult(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    # subject field hata di, taake errors na aaye
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.marks_obtained}/{self.total_marks}"
