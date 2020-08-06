from django.urls import path, include
from rest_framework_nested import routers
from meetings.views import MeetingClassViewset, MeetingStateViewset, MeetingTypeViewset, AuditorsMeetingViewset, CustomersMeetingViewset
from users.urls import router as routerUsers

router = routers.SimpleRouter()

router.register(r"MeetingClasses", MeetingClassViewset)
router.register(r"MeetingTypes", MeetingTypeViewset)
router.register(r"MeetingStates", MeetingStateViewset)

auditor_router = routers.NestedSimpleRouter(routerUsers, r'Staff', lookup='auditor')
auditor_router.register(r'Meetings', AuditorsMeetingViewset, basename='auditors-meetings')

customer_router = routers.NestedSimpleRouter(routerUsers, r'Customers', lookup='customer')
customer_router.register(r'Meetings', CustomersMeetingViewset, basename='customers-meetings')



urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(auditor_router.urls)),
    path('api/', include(customer_router.urls))
]