from rest_framework.permissions import BasePermission
from users.models import User, Position


class IsMeetingAuditor(BasePermission):
    
    message = 'User is not the auditor of the meeting'

    def has_obj_permission(self, request, view, obj):
        
        has_permission = False
        user = request.user
        if obj.auditor == user.id:
            has_permission = True
        return has_permission

class IsMeetingCustomer(BasePermission):
    
    message = 'User is not the customer of the meeting'

    def has_obj_permission(self, request, view, obj):
        
        has_permission = False
        user = request.user
        if obj.customer == user.id:
            has_permission = True
        return has_permission

class IsCustomerOwner(BasePermission):

    """
    permission to only allow owners of a customer account to list its relations.
    """

    message = "user making the request is not the owner of this account"

    def has_permission(self, request, view):
        has_permission = False
        if not request.user.is_staff and not request.user.is_superuser:
            if request.user.id == (int)(view.kwargs["customer_pk"]):
                has_permission = True
            else:
                has_permission = False
        return has_permission

class IsAuditorOwner(BasePermission):

    """
    permission to only allow owners of an auditor account to list its relations.
    """

    message = "user making the request is not the owner of this account"
    
    def has_permission(self, request, view):
        has_permission = False
        if request.user.is_staff:
            if request.user.id == (int)(view.kwargs["auditor_pk"]):
                has_permission = True

                if view.action == "create" and "auditor" in request.data and  not request.data["auditor"] == request.user.id:
                    has_permission = False
                    self.message = "Auditor sent in data is not the same auditor on url"
            elif request.user.is_superuser:
                has_permission = True
            else:
                has_permission = False
        return has_permission




