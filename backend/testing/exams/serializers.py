from rest_framework import serializers
from .models import Exam, ExamResult

# ===================== Simple Exam Serializer =====================
class ExamSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True)
    campus_name = serializers.CharField(source='campus.campus_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Exam
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validate passing marks
        if 'passing_marks' in data and 'total_marks' in data:
            if data['passing_marks'] > data['total_marks']:
                raise serializers.ValidationError("Passing marks cannot be greater than total marks")
        
        return data

# ===================== Simple Exam Result Serializer =====================
class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    exam_name = serializers.CharField(source='exam.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    # Computed fields
    percentage = serializers.ReadOnlyField()
    is_pass = serializers.ReadOnlyField()
    
    class Meta:
        model = ExamResult
        fields = '__all__'
        read_only_fields = ['percentage', 'is_pass', 'created_at', 'updated_at']

    def validate(self, data):
        # Validate marks
        if 'marks_obtained' in data and 'total_marks' in data:
            if data['marks_obtained'] > data['total_marks']:
                raise serializers.ValidationError("Marks obtained cannot be greater than total marks")
            
            if data['marks_obtained'] < 0:
                raise serializers.ValidationError("Marks obtained cannot be negative")
        
        return data

# ===================== Bulk Operations =====================
class BulkExamResultSerializer(serializers.Serializer):
    """Serializer for bulk exam result operations"""
    exam_id = serializers.IntegerField()
    results = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    
    def validate_results(self, value):
        required_fields = ['student_id', 'subject_id', 'marks_obtained', 'total_marks']
        for result in value:
            for field in required_fields:
                if field not in result:
                    raise serializers.ValidationError(f"Missing required field: {field}")
        return value
