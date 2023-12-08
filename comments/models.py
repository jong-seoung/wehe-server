from django.db import models
from core.models import TimeStampedModel
from user.models import User
from posts.models import Post


class Comment(TimeStampedModel, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
