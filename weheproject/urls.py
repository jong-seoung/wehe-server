from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.registration.views import VerifyEmailView

from weheproject.swagger import get_swagger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('static/<path:dummy>', serve, {'document_root': settings.STATIC_ROOT}),
    path("api/v1/user/", include("user.urls")),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_confirm_email_sent",
    ),
    path(
        "account-confirm-email/<key>/",
        VerifyEmailView.as_view(),
        name="account_confirm_email",
    ),
]

if settings.DEBUG:
    urlpatterns += get_swagger_urls()
