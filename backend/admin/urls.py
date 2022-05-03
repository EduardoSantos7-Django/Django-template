from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/docs')),
    path('', api.urls),
]
