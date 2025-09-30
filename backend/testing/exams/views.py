from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.utils import timezone

from .models import Exam, ExamResult
from .serializers import ExamSerializer, ExamResultSerializer, BulkExamResultSerializer

# ===================== Simple Exam ViewSet =====================
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('grade', 'classroom', 'campus', 'created_by')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'academic_year']
    filterset_fields = ['exam_type', 'grade', 'classroom', 'campus', 'academic_year', 'is_active', 'is_published']
    ordering_fields = ['exam_date', 'created_at', 'name']
    ordering = ['-exam_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by campus if user has campus restriction
        if hasattr(self.request.user, 'campus') and self.request.user.campus:
            queryset = queryset.filter(campus=self.request.user.campus)
        
        return queryset

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming exams"""
        queryset = self.get_queryset().filter(
            exam_date__gte=timezone.now().date(),
            is_active=True
        ).order_by('exam_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_grade(self, request):
        """Get exams by grade"""
        grade_id = request.query_params.get('grade_id')
        if not grade_id:
            return Response({'error': 'grade_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(grade_id=grade_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def publish_results(self, request, pk=None):
        """Publish exam results"""
        exam = self.get_object()
        exam.is_published = True
        exam.save()
        return Response({'message': 'Results published successfully'})

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get exam statistics"""
        exam = self.get_object()
        
        # Basic statistics
        total_students = 0
        if exam.classroom:
            total_students = exam.classroom.students.count()
        
        # Result statistics
        results = ExamResult.objects.filter(exam=exam)
        total_results = results.count()
        
        if total_results > 0:
            avg_percentage = results.aggregate(avg=Avg('percentage'))['avg'] or 0
            pass_count = results.filter(is_pass=True).count()
            fail_count = total_results - pass_count
            
            # Grade distribution
            grade_distribution = results.values('grade').annotate(
                count=Count('id')
            ).order_by('-count')
        else:
            avg_percentage = 0
            pass_count = 0
            fail_count = 0
            grade_distribution = []
        
        return Response({
            'total_students': total_students,
            'total_results': total_results,
            'average_percentage': round(avg_percentage, 2),
            'pass_count': pass_count,
            'fail_count': fail_count,
            'grade_distribution': list(grade_distribution)
        })

# ===================== Simple Exam Result ViewSet =====================
class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.select_related('student', 'exam', 'subject')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student__name', 'student__student_code', 'subject__name']
    filterset_fields = ['exam', 'student', 'subject', 'is_pass', 'grade']
    ordering_fields = ['marks_obtained', 'percentage', 'created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def by_exam(self, request):
        """Get results by exam"""
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response({'error': 'exam_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(exam_id=exam_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """Get results by student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = self.get_queryset().filter(student_id=student_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create exam results"""
        serializer = BulkExamResultSerializer(data=request.data)
        if serializer.is_valid():
            exam_id = serializer.validated_data['exam_id']
            results_data = serializer.validated_data['results']
            
            created_results = []
            for result_data in results_data:
                result = ExamResult.objects.create(
                    exam_id=exam_id,
                    student_id=result_data['student_id'],
                    subject_id=result_data['subject_id'],
                    marks_obtained=result_data['marks_obtained'],
                    total_marks=result_data['total_marks']
                )
                created_results.append(result)
            
            response_serializer = ExamResultSerializer(created_results, many=True)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
