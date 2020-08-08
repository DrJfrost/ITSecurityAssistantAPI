from reports_management.models import System, Report, SystemType, ReportState, AttackType, Complexity, OperatingSystem
from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from meetings.permissions import IsAuditorOwner
from users.permissions import IsSuperUser, IsAuditor, IsAnalyst, DenyPermission, IsAnalystOwner, IsCustomer, IsCustomerOwner
from reports_management.permissions import IsReportAnalyst, IsReportAuditor, IsSystemCustomer, CheckMeetingInfo
from reports_management.serializers import SystemSerializer, SystemNestedSerializer, ReportSerializer, ReportNestedSerializer, AttackTypeSerializer, AttackTypeNestedSerializer, OperatingSystemSerializer, SystemTypeSerializer, ReportStateSerializer, ComplexitySerializer


# Create your views here.
class SystemViewSet(viewsets.ModelViewSet):
    queryset=System.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SystemNestedSerializer
        return SystemSerializer

class ReportViewSet(viewsets.ModelViewSet):
    queryset=Report.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer

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
    

class AuditorsReportViewSet(viewsets.ModelViewSet):
    
    def get_permissions(self):
        permission_classes = []
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAuditor, IsAuditorOwner]

        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAuditor, IsReportAuditor, IsAuditorOwner]
        
        elif self.action == 'create':
            permission_classes = [DenyPermission]
        
        elif self.action == 'update':
            permission_classes = [DenyPermission]

        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    def  get_queryset(self):
        queryset=Report.objects.filter(auditor=self.kwargs['auditor_pk'])
        print (queryset.query)
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer   



class CustomerMeetingReportViewSet(viewsets.GenericViewSet, generics.RetrieveAPIView):
    
    permission_classes = [IsAuthenticated, IsCustomer, IsCustomerOwner]
    serializer_class = ReportNestedSerializer

    def get_queryset(self):
        queryset = Report.objects.filter(meeting=self.kwargs['meeting_pk'], meeting__customer=self.kwargs['customer_pk'], meeting__state="Finished")
        return queryset

class AnalystReportViewSet(viewsets.ModelViewSet):
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """

        permission_classes = []

        if self.action == 'list':
            permission_classes = [(IsAuthenticated & IsAnalyst & IsAnalystOwner) | IsSuperUser]

        elif self.action == 'retrieve':
            permission_classes = [(IsAuthenticated & IsAnalyst & IsReportAnalyst & IsAnalystOwner) | IsSuperUser]

        elif self.action == 'create':
            permission_classes = [(IsAuthenticated & IsAnalyst & CheckMeetingInfo & IsAnalystOwner) | IsSuperUser]
        
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [DenyPermission]

        elif self.action == 'destroy':
            permission_classes = [DenyPermission]
        return [permission() for permission in permission_classes]

    def  get_queryset(self):
        queryset=Report.objects.filter(analyst = self.kwargs['analyst_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer   
    

class ReportAttackTypeViewSet(viewsets.ModelViewSet):
    

    def get_permissions(self):

        permission_classes = []

        if self.action == 'list':
            permission_classes = [AllowAny]

        elif self.action == 'retrieve':
            permission_classes = [AllowAny]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAnalyst]

        return [permission() for permission in permission_classes]

    def  get_queryset(self):
        queryset=Report.objects.filter(auditor = self.kwargs['report_pk'])
        return queryset
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ReportNestedSerializer
        return ReportSerializer   

class AttackTypeViewSet(viewsets.ModelViewSet):#que se adue~no del reporte is report owner and auditor que el id del analista sea el del request 
    queryset=AttackType.objects.all()

    def get_permissions(self):
        permission_classes = []

        if self.action == 'list':
            permission_classes = [AllowAny]

        elif self.action == 'retrieve':
            permission_classes = [AllowAny]

        elif self.action == 'create':
            permission_classes = [IsAuthenticated & (IsAnalyst | IsSuperUser)]

        elif self.action == 'update' or self.action == 'partial_update':
                permission_classes = [DenyPermission]

        elif self.action == 'destroy':
                permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method  in SAFE_METHODS:
            return AttackTypeNestedSerializer
        return AttackTypeSerializer

class CustomersSystemViewset(viewsets.ModelViewSet):

    permission_classes = []
    
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [(IsAuthenticated & IsCustomer & IsCustomerOwner) | IsSuperUser | IsAnalyst | IsAuditor]
        elif self.action == 'retrieve':
            permission_classes = [(IsAuthenticated & IsCustomer & IsSystemCustomer & IsCustomerOwner) | IsSuperUser]
        elif self.action == 'create':
            permission_classes = [(IsAuthenticated & IsCustomer & IsCustomerOwner) | IsSuperUser]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [DenyPermission]#opcional
        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = System.objects.filter(customer=self.kwargs['customer_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return SystemNestedSerializer
        return SystemSerializer


