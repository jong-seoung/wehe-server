from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("post/", views.PostAPI.as_view(), name="post-list"),
    path("post/<int:pk>/", views.PostDetailAPI.as_view(), name="post-detail"),
    path("post/<int:pk>/like/", views.PostLikeAPI.as_view(), name="post-like"),
]
