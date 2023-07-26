from django.db import models
from core.models import TimeStampedModel
from skills.models import Skill
from user.models import User


class Post(TimeStampedModel, models.Model):
    title = models.CharField(max_length=256)
    schedule = models.CharField(max_length=35)
    deadline = models.DateField()
    role = models.CharField()
    skills = models.ManyToManyField(Skill)
    contact = models.CharField()
    contact_url = models.TextField()
    views = models.PositiveIntegerField(default=0)

    is_private = models.BooleanField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "posts"
        db_table_comment = "작성글 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["author"]),
        ]


class Like(TimeStampedModel, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "post")
