from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostListAPI.as_view(), name="post-list"),
    path("create/", views.PostCreateAPI.as_view(), name="post-create"),
    path("popular/", views.PopularPostAPI.as_view(), name="popular-post"),
    path("detail/<int:post_id>/", views.PostDetailAPI.as_view(), name="post-detail"),
    path("<int:post_id>/like/", views.PostLikeAPI.as_view(), name="post-like"),
]
