from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def get_swagger_urls():
    schema_view = get_schema_view(
        openapi.Info(
            title="weheproject API",
            default_version="v1",
            description="API for weheproject",
            terms_of_service="https://github.com/orgs/Team-We-Here/repositories",
        ),
        validators=["flex"],
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    return [
        path(
            "swagger.<str:format>",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
