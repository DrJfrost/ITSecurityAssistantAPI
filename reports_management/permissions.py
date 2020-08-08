from rest_framework.permissions import BasePermission
from users.models import User, Position
from meetings.models import Meeting

class IsReportAuditor(BasePermission):
    
    message = 'User is not the auditor of the report'

    def has_obj_permission(self, request, view, obj):
        
        has_permission = False
        user = request.user
        if obj.auditor == user.id:
            has_permission = True
        return has_permission

class IsReportAnalyst(BasePermission):
    
    message = 'User is not the analyst of the report'

    def has_obj_permission(self, request, view, obj):
        
        has_permission = False
        user = request.user
        if obj.analyst == user.id:
            has_permission = True
        return has_permission

class IsSystemCustomer(BasePermission):
    
    message = 'User is not the customer of the system'

    def has_obj_permission(self, request, view, obj):
        
        has_permission = False
        user = request.user
        if obj.customer == user.id:
            has_permission = True
        return has_permission

class CheckCustomer(BasePermission):
    message = "Customer on meeting is not the same customer in data"

    def has_permission(self, request, view):
        has_permission = False

        meeting_id = request.data["meeting"]#Se obtiene el id del json que se envia en post
        meeting = Meeting.objects.get(pk = meeting_id)#Se obtiene objeto Meeting usando el pk
        auditor_id= meeting.auditor.id#se saca el id del auditor del obejto meeting

        if auditor_id == request.data["auditor"]:
            has_permission = True
        else:
            has_permission = False

        return has_permission