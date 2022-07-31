from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='/docs/'), name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    # OpenAPI Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    # Routes
    path('admin/', admin.site.urls),
    path('account/', include('authentication.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
