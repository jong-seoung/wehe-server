from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from user.social_views.google_login import (
    GoogleLoginView,
    GoogleCallbackView,
    GoogleLoginToDjango,
)
from user.social_views.kakao_login import (
    KakaoLoginView,
    KakaoCallbackView,
    KakaoLoginToDjango,
)
from user.social_views.github_login import (
    GithubLoginView,
    GithubCallbackView,
    GithubLoginToDjango,
)
from .views import LogoutAPIView


urlpatterns = [
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path("google/callback/", GoogleCallbackView.as_view(), name="google_callback"),
    path(
        "google/login/finish/",
        GoogleLoginToDjango.as_view(),
        name="google_login_to_django",
    ),
    path("kakao/login/", KakaoLoginView.as_view(), name="kakao_login"),
    path("kakao/callback/", KakaoCallbackView.as_view(), name="kakao_callback"),
    path(
        "kakao/login/finish/",
        KakaoLoginToDjango.as_view(),
        name="kakao_login_to_django",
    ),
    path("github/login/", GithubLoginView.as_view(), name="github_login"),
    path("github/callback/", GithubCallbackView.as_view(), name="github_callback"),
    path(
        "github/login/finish/",
        GithubLoginToDjango.as_view(),
        name="github_login_to_django",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
]
