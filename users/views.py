from django.shortcuts import render
from users.models import Identification, StaffProfile, User, Position
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from users.permissions import IsOwner, DenyPermission, IsSuperUser, IsAdminUser
from users.serializers import StaffUserNestedSerializer, CustomerUserNestedSerializer

# Views.

class CustomerUserViewset(viewsets.ModelViewSet):

    queryset = User.objects.filter(is_superuser=False, is_staff=False)

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsAuthenticated & IsAdminUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & (IsAdminUser | IsOwner)]
        elif self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsSuperUser]
        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]

    serializer_class = CustomerUserNestedSerializer

class StaffUserViewset(viewsets.ModelViewSet):

    queryset = User.objects.filter(is_superuser=False, is_staff=True)
    serializer_class = StaffUserNestedSerializer

    def get_permissions(self):

        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permission_classes = []

        if self.action == 'list':
            permission_classes = [IsSuperUser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated & IsOwner]
        elif self.action == 'create':
            permission_classes = [IsSuperUser]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsSuperUser]
        elif self.action == 'destroy':
            permission_classes = [DenyPermission]

        return [permission() for permission in permission_classes]
