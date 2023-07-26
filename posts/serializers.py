from posts.models import Post
from posts.models import Like
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_nickname",
            "schedule",
            "deadline",
            "role",
            "skills",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
        ]

    author_nickname = serializers.SerializerMethodField("get_author_nickname")
    like_count = serializers.SerializerMethodField("get_like_count")

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_like_count(self, obj):
        like_count = Like.objects.filter(post=obj).count()
        return like_count


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_nickname",
            "schedule",
            "deadline",
            "role",
            "skills",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
        ]

    author_nickname = serializers.SerializerMethodField("get_author_nickname")
    like_count = serializers.SerializerMethodField("get_like_count")

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_like_count(self, obj):
        like_count = Like.objects.filter(post=obj).count()
        return like_count
