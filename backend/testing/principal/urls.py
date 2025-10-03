from rest_framework.routers import DefaultRouter
from .views import PrincipalViewSet

router = DefaultRouter()
router.register(r"principals", PrincipalViewSet)

urlpatterns = router.urls
