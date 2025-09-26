from rest_framework import viewsets
from .models import AttendanceType, AttendanceRegister, AttendanceSheet, AttendanceLine
from .serializers import (
    AttendanceTypeSerializer,
    AttendanceRegisterSerializer,
    AttendanceSheetSerializer,
    AttendanceLineSerializer,
)


class AttendanceTypeViewSet(viewsets.ModelViewSet):
    queryset = AttendanceType.objects.all()
    serializer_class = AttendanceTypeSerializer


class AttendanceRegisterViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRegister.objects.all()
    serializer_class = AttendanceRegisterSerializer


class AttendanceSheetViewSet(viewsets.ModelViewSet):
    queryset = AttendanceSheet.objects.all()
    serializer_class = AttendanceSheetSerializer


class AttendanceLineViewSet(viewsets.ModelViewSet):
    queryset = AttendanceLine.objects.all()
    serializer_class = AttendanceLineSerializer
