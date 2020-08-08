from django.shortcuts import render
from meetings.models import MeetingClass, MeetingState, MeetingType, Meeting
from rest_framework import viewsets, generics, mixins
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser, AllowAny
from users.permissions import IsAuditor, DenyPermission, IsCustomer
from meetings.permissions import IsMeetingAuditor, IsMeetingCustomer, IsCustomerOwner, IsAuditorOwner, CheckAuditor
from meetings.serializers import MeetingClassSerializer, MeetingStateSerializer, MeetingTypeSerializer, MeetingInfoSerializer, MeetingSerializer

#Views.

class MeetingClassViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = MeetingClassSerializer
    queryset = MeetingClass.objects.all()
    permission_classes = [AllowAny]

class MeetingStateViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = MeetingStateSerializer
    queryset = MeetingState.objects.all()
    permission_classes = [AllowAny] 

class MeetingTypeViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = MeetingTypeSerializer
    queryset = MeetingType.objects.all()
    permission_classes = [AllowAny]

class AuditorsMeetingViewset(viewsets.ModelViewSet):

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAuditor, IsAuditorOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAuditor, IsMeetingAuditor, IsAuditorOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAuditor, IsAuditorOwner]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAuditor]
        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Meeting.objects.filter(auditor=self.kwargs['auditor_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MeetingInfoSerializer
        return MeetingSerializer

class PendingMeetingsViewset(viewsets.GenericViewSet, generics.RetrieveUpdateAPIView, mixins.ListModelMixin):
    
    queryset = Meeting.objects.filter(auditor=None)

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsAuditor]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsAuditor]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAuthenticated, IsAuditor, CheckAuditor]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MeetingInfoSerializer
        return MeetingSerializer

class CustomersMeetingViewset(viewsets.ModelViewSet):
    
    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsCustomer, IsCustomerOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsCustomer, IsMeetingCustomer, IsCustomerOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsCustomer, IsCustomerOwner]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [DenyPermission]
        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Meeting.objects.filter(customer=self.kwargs['customer_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MeetingInfoSerializer
        return MeetingSerializer


class CustumerSystemViewset(viewsets.ModelViewSet):
    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsCustomer, IsCustomerOwner]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsCustomer, IsMeetingCustomer, IsCustomerOwner]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Meeting.objects.filter(customer=self.kwargs['customer_pk'])
        return queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MeetingInfoSerializer
        return MeetingSerializer
