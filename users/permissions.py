from rest_framework.permissions import BasePermission
from users.models import User, Position


class IsAuditor(BasePermission):
    
    message = 'User is not an auditor'

    def has_permission(self, request, view):
        
        has_permission = False
        user = request.user
        if user.is_staff and user.staff_profile.position.name == 'Auditor':
            has_permission = True
        return has_permission

class IsAnalyst(BasePermission):
    
    message = 'User is not an analyst'

    def has_permission(self, request, view):
        has_permission = False
        user = request.user
        if user.is_staff and user.staff_profile.position.name == 'Analyst':
            has_permission = True
        return has_permission

class IsCustomer(BasePermission):
    
    message = 'User is not a customer'

    def has_permission(self, request, view):
        
        has_permission = False
        user = request.user
        if not user.is_staff and not user.is_superuser:
            has_permission = True
        return has_permission

class IsSuperUser(BasePermission):
    
    message = 'User is not a superuser'

    def has_permission(self, request, view):
        
        has_permission = False
        user = request.user
        if user.is_staff and user.is_superuser:
            has_permission = True
        return has_permission

class IsOwner(BasePermission):
    
    message = 'User is not the owner of this account'

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        
        has_permission = False
        if request.user.id == obj.id:
            has_permission = True
        return has_permission

class DenyPermission(BasePermission):

    def has_permission(self, request, view):
        return False

class IsAdminUser(BasePermission):

    message = 'User is not an Admin'

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff 

class IsAnalystOwner(BasePermission):

    """
    permission to only allow owners of an auditor account to list its relations.
    """

    message = "User making the request is not the owner of this account"

    def has_permission(self, request, view):
        has_permission = False
        if request.user.is_staff:
            if request.user.id == (int)(view.kwargs["analyst_pk"]):
                has_permission = True
                if view.action == "create" and "analyst" in request.data and request.data["analyst"] != request.user.id:
                    has_permission = False
                    self.message = "Analyst sent in data is not the same analyst on url"
            elif request.user.is_superuser:
                has_permission = True
            else:
                has_permission = False
        return has_permission

class IsCustomerOwner(BasePermission):

    """
    permission to only allow owners of an auditor account to list its relations.
    """
    message = "user making the request is not the owner of this account"

    def has_permission(self, request, view):
        has_permission = False
        if not request.user.is_staff:
            if request.user.id == (int)(view.kwargs["customer_pk"]):
                has_permission = True
                if view.action == "create" and "customer" in request.data and not request.data["customer"] == request.user.id:
                    has_permission = False
                    self.message = "Customer sent in data is not the same customer on url"
            elif request.user.is_superuser:
                has_permission = True
            else:
                has_permission = False
        return has_permission