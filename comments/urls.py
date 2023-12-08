from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("<int:post_id>/", views.CommentCreateAPI.as_view(), name="comment-create"),
    path("<int:post_id>/<int:comment_id>/", views.CommentDetailAPI.as_view(), name="comment-detail"),
]
