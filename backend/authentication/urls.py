from django.db import router
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('', views.AuthViewSet, basename='auth')
router.register('', views.AuthTokenViewset, basename='token')

urlpatterns = router.urls
