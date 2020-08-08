from django.urls import path, include
from rest_framework import routers
from users.views import CustomerUserViewset, StaffUserViewset

router = routers.SimpleRouter()
router.register(r'Customers', CustomerUserViewset)
router.register(r'Auditors', StaffUserViewset)
router.register(r'Analysts', StaffUserViewset)


urlpatterns = [
    path('api/', include(router.urls))
]