from django.urls import path

from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("google/login/", views.GoogleLoginView.as_view(), name="google_login"),
    path(
        "google/callback/", views.GoogleCallbackView.as_view(), name="google_callback"
    ),
    path(
        "google/login/finish/",
        views.GoogleLoginToDjango.as_view(),
        name="google_login_to_django",
    ),
    path("kakao/login/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", views.KakaoCallbackView.as_view(), name="kakao_callback"),
    path(
        "kakao/login/finish/",
        views.KakaoLoginToDjango.as_view(),
        name="kakao_login_to_django",
    ),
    path("github/login/", views.GithubLoginView.as_view(), name="github_login"),
    path(
        "github/callback/", views.GithubCallbackView.as_view(), name="github_callback"
    ),
    path(
        "github/login/finish/",
        views.GithubLoginToDjango.as_view(),
        name="github_login_to_django",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
]
