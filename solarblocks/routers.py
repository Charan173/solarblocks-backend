from rest_framework.routers import DefaultRouter

from projects.viewsets import ProjectViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')

urlpatterns = router.urls