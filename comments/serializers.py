from comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "author_nickname",
            "content",
            "created_at",
            "updated_at",
        ]

    author_nickname = serializers.SerializerMethodField("get_author_nickname")

    def get_author_nickname(self, obj):
        return obj.author.nickname
