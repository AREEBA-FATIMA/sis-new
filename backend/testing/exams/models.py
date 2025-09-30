from django.db import models
from django.utils import timezone

# ===================== Simple Exam Model =====================
class Exam(models.Model):
    EXAM_TYPE_CHOICES = [
        ('mid_term', 'Mid Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('test', 'Test'),
    ]
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES, default='test')
    academic_year = models.CharField(max_length=20)
    campus = models.ForeignKey("campus.Campus", on_delete=models.CASCADE)
    grade = models.ForeignKey("classes.Grade", on_delete=models.CASCADE, null=True, blank=True)
    classroom = models.ForeignKey("classes.ClassRoom", on_delete=models.CASCADE, null=True, blank=True)
    
    # Basic Exam Details
    exam_date = models.DateField()
    total_marks = models.FloatField(default=100.0)
    passing_marks = models.FloatField(default=33.0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    
    # System Fields
    created_by = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-exam_date']
        unique_together = ['name', 'academic_year', 'campus', 'grade']

    def __str__(self):
        return f"{self.name} - {self.grade} ({self.exam_date})"

# ===================== Simple Exam Result Model =====================
class ExamResult(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey("subjects.Subject", on_delete=models.CASCADE)
    
    # Marks
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    percentage = models.FloatField(editable=False)
    is_pass = models.BooleanField(default=False)
    
    # Grade (Simple)
    grade = models.CharField(max_length=5, blank=True, null=True)
    
    # Additional Info
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam', 'subject']
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Calculate percentage
        if self.total_marks > 0:
            self.percentage = (self.marks_obtained / self.total_marks) * 100
        else:
            self.percentage = 0.0
        
        # Determine pass/fail
        self.is_pass = self.marks_obtained >= self.exam.passing_marks
        
        # Simple grade assignment
        if not self.grade:
            if self.percentage >= 90:
                self.grade = 'A+'
            elif self.percentage >= 80:
                self.grade = 'A'
            elif self.percentage >= 70:
                self.grade = 'B+'
            elif self.percentage >= 60:
                self.grade = 'B'
            elif self.percentage >= 50:
                self.grade = 'C'
            elif self.percentage >= 40:
                self.grade = 'D'
            else:
                self.grade = 'F'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.exam.name} - {self.subject.name}: {self.marks_obtained}/{self.total_marks}"
