from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from weheproject.swagger import get_swagger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/user/", include("user.urls")),
]

if settings.DEBUG:
    urlpatterns += get_swagger_urls()
