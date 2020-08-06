from reports_management.models import System, Report, SystemType, ReportState, AttackType, Complexity, OperatingSystem
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from reports_management.serializers import SystemSerializer, SystemNestedSerializer, ReportSerializer, ReportNestedSerializer, AttackTypeSerializer, AttackTypeNestedSerializer, OperatingSystemSerializer, SystemTypeSerializer, ReportStateSerializer, ComplexitySerializer


# Create your views here.
class SystemViewSet(viewsets.ModelViewSet):
    queryset=System.objects.all()
#for gets
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SystemNestedSerializer
        return SystemSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset=Report.objects.all()
#for gets
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer
#
class AuditorsReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    def  get_queryset(self):
        queryset=Report.objects.filter(auditor = self.kwargs['auditor_pk'])
        return queryset

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsAuditorUser]
        else:
            permission_classes = [IsAuditorUser]

        return [permission() for permission in permission_classes]

#for gets
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer

class AnalystReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def  get_queryset(self):
        queryset=Report.objects.filter(auditor = self.kwargs['analyst_pk'])
        return queryset

    def get_permissions(self):

        if self.action == 'list':
            permission_classes = [IsAnalystUser]
        else:
            permission_classes = [IsAnalystUser]

        return [permission() for permission in permission_classes]

class ReportAttackTypeComplexity(viewsets.ModelViewSet):
    def  get_queryset(self):
        queryset=Report.objects.filter(auditor = self.kwargs['report_pk'])
        return queryset
#aca van los permisos????
    
#for gets
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer

class AttackTypeViewSet(viewsets.ModelViewSet):#que se adue~no del reporte is report owner and auditor que el id del analista sea el del request 
    queryset=AttackType.objects.all()
#for gets
    def get_serializer_class(self):
        if self.request.method  in SAFE_METHODS:
            return AttackTypeNestedSerializer
        return AttackTypeSerializer

class OperatingSystemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OperatingSystemSerializer
    queryset=OperatingSystem.objects.all()
    

class SystemTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SystemTypeSerializer
    queryset=SystemType.objects.all()
    

class ReportStateViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReportStateSerializer
    queryset=ReportState.objects.all()
    

class ComplexityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ComplexitySerializer
    queryset=Complexity.objects.all()
    
