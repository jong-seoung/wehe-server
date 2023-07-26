from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("", views.CommentListAPI.as_view(), name="comment-list"),
    path("<int:post_pk>/", views.CommentCreateAPI.as_view(), name="comment-create"),
    path("<int:pk>/", views.CommentDetailAPI.as_view(), name="comment-detail"),
]
