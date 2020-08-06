from django.urls import path, include
from rest_framework_nested import routers
from reports_management.views import SystemViewSet, ReportViewSet, OperatingSystemViewSet, ComplexityViewSet,AttackTypeViewSet, SystemTypeViewSet,ReportStateViewSet
from users.urls import router as routerReportUser
router = routers.SimpleRouter()

router.register(r"Complexities",ComplexityViewSet)
router.register(r"AttackTypes", AttackTypeViewSet)
router.register(r"SystemTypes", SystemTypeViewSet)
router.register(r"ReportStates", ReportStateViewSet)

auditor_router = routers.NestedSimpleRouter(routerUsers, r'Staff', lookup='auditor')
auditor_router.register(r'Report',AuditorsReportViewSet, base_name='auditors-reports')

auditor_router = routers.NestedSimpleRouter(routerUsers, r'Staff', lookup='analyst')
auditor_router.register(r'Report',AuditorsReportViewSet, base_name='analyst-reports')


urlpatterns = [
    path('api/', include (router.urls)),
    path('api/', include (auditor_router.urls)),
    path('api/', include (analyst_router.urls)),
]