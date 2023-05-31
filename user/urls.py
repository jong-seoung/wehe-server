from django.urls import path, include
from .views import LogoutView, KakaoLoginView, GoogleLoginView, GithubLoginView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/kakao/login', KakaoLoginView.as_view(), name='kakao login'),
    path('accounts/google/login', GoogleLoginView.as_view(), name='google login'),
    path('accounts/github/login', GithubLoginView.as_view(), name='github login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
