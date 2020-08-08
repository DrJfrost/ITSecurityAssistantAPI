from django.urls import path, include
from rest_framework_nested import routers
from reports_management.views import ComplexityViewSet, SystemTypeViewSet, OperatingSystemViewSet, AttackTypeViewSet, ReportStateViewSet, AuditorsReportViewSet, AnalystReportViewSet, CustomersSystemViewset
from users.urls import router as routerReportUser

router = routers.SimpleRouter()

router.register(r"Complexities",ComplexityViewSet)
router.register(r"AttackTypes", AttackTypeViewSet)
router.register(r"SystemTypes", SystemTypeViewSet)
router.register(r"ReportStates", ReportStateViewSet)
router.register(r"OperatingSystems", OperatingSystemViewSet)


auditor_router = routers.NestedSimpleRouter(routerReportUser, r'Auditors', lookup='auditor')
auditor_router.register(r'Reports',AuditorsReportViewSet, basename='auditor-reports')

analyst_router = routers.NestedSimpleRouter(routerReportUser, r'Analysts', lookup='analyst')
analyst_router.register(r'Reports',AnalystReportViewSet, basename = 'analyst-reports')

customer_router = routers.NestedSimpleRouter(routerReportUser, r'Customers', lookup='customer')
customer_router.register(r'Systems', CustomersSystemViewset, basename='customers-system')


urlpatterns = [
    path('api/', include (router.urls)),
    path('api/', include (auditor_router.urls)),
    path('api/', include (analyst_router.urls)),
    path('api/', include (customer_router.urls))
]