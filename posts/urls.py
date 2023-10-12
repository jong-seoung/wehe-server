from django.urls import path, include
from . import views

app_name = "posts"

urlpatterns = [
    path("<int:page>/", views.PostAPI.as_view(), name="post-list"),
    path("popular/", views.PopularPostAPI.as_view(), name="popular-post"),
    path("detail/<int:post_id>/", views.PostDetailAPI.as_view(), name="post-detail"),
    path("<int:post_id>/like/", views.PostLikeAPI.as_view(), name="post-like"),
]
