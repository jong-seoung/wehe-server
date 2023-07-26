from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostAPI.as_view(), name="post-list"),
    path("<int:pk>/", views.PostDetailAPI.as_view(), name="post-detail"),
    path("<int:pk>/like/", views.PostLikeAPI.as_view(), name="post-like"),
]
