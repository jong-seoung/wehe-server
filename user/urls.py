from django.urls import path, include
from user.views import LoginView


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('login/', LoginView.as_view(), name="login view"),
]
