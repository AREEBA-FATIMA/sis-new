from django.contrib import admin
from .models import Exam, ExamResult

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'exam_type', 'grade', 'classroom', 'campus', 
        'exam_date', 'total_marks', 'is_active', 'is_published'
    ]
    list_filter = [
        'exam_type', 'grade', 'campus', 'academic_year', 
        'is_active', 'is_published', 'exam_date'
    ]
    search_fields = ['name', 'academic_year']
    ordering = ['-exam_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'exam_type', 'academic_year', 'campus')
        }),
        ('Grade & Class', {
            'fields': ('grade', 'classroom')
        }),
        ('Exam Details', {
            'fields': ('exam_date', 'total_marks', 'passing_marks')
        }),
        ('Status', {
            'fields': ('is_active', 'is_published')
        }),
        ('System', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = [
        'student', 'exam', 'subject', 'marks_obtained', 'total_marks', 
        'percentage', 'grade', 'is_pass', 'created_at'
    ]
    list_filter = [
        'exam', 'subject', 'is_pass', 'grade', 'created_at'
    ]
    search_fields = [
        'student__name', 'student__student_code', 'subject__name', 'exam__name'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Student & Exam', {
            'fields': ('student', 'exam', 'subject')
        }),
        ('Marks', {
            'fields': ('marks_obtained', 'total_marks', 'percentage')
        }),
        ('Grade', {
            'fields': ('grade', 'is_pass')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ['percentage', 'is_pass', 'created_at', 'updated_at']
