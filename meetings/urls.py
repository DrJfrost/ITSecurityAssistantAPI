from django.urls import path, include
from rest_framework_nested import routers
from meetings.views import MeetingClassViewset, MeetingStateViewset, MeetingTypeViewset, AuditorsMeetingViewset, CustomersMeetingViewset, PendingMeetingsViewset
from users.urls import router as routerUsers
from reports_management.views import CustomerMeetingReportViewSet

router = routers.SimpleRouter()

router.register(r"MeetingClasses", MeetingClassViewset)
router.register(r"MeetingTypes", MeetingTypeViewset)
router.register(r"MeetingStates", MeetingStateViewset)
router.register(r"Pendingmeetings", PendingMeetingsViewset)


auditor_router = routers.NestedSimpleRouter(routerUsers, r'Auditors', lookup='auditor')
auditor_router.register(r'Meetings', AuditorsMeetingViewset, basename='auditors-meetings')

customer_router = routers.NestedSimpleRouter(routerUsers, r'Customers', lookup='customer')
customer_router.register(r'Meetings', CustomersMeetingViewset, basename='customers-meetings')

report_router = routers.NestedSimpleRouter(customer_router, r'Meetings', lookup='meeting')
report_router.register(r'Report', CustomerMeetingReportViewSet, basename='customers-meetings-report')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(auditor_router.urls)),
    path('api/', include(customer_router.urls)),
    path('api/', include(report_router.urls))
]