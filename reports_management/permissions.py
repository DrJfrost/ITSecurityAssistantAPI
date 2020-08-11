from rest_framework.permissions import BasePermission
from users.models import User, Position
from meetings.models import Meeting
from reports_management.models import System

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

class CheckMeetingInfo(BasePermission):
    message = "meeting auditor is not the same as the auditor in request data."

    def has_permission(self, request, view):
        has_permission = False

        if "meeting" in request.data:
            meeting_id = request.data["meeting"]#Se obtiene el id del json que se envia en post
            meeting = Meeting.objects.get(pk=meeting_id)#Se obtiene objeto Meeting usando el pk
            auditor_id = meeting.auditor.id#se saca el id del auditor del obejto meeting
            if "auditor" in request.data and auditor_id == (int)(request.data["auditor"]):
                has_permission = True
            elif not "auditor" in request.data:
                has_permission = True
            else:
                has_permission = False
            
            if "system" in request.data:
                system_id = request.data["system"]#Se obtiene el id del json que se envia en post
                system = System.objects.get(pk=system_id)#Se obtiene objeto System usando el pk
                if system.customer.id != meeting.customer.id:
                    self.message = "the system you are trying to report does not belong to the customer that created meeting"
                    has_permission = False
        else:
            has_permission = True


        return has_permission