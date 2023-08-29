from posts.models import Post, Like
from skills.models import Skill
from roles.models import Role
from rest_framework import serializers
from comments.serializers import CommentSerializer


class PostSerializerBase(serializers.ModelSerializer):
    skills_list = serializers.SerializerMethodField("get_skills_list")
    roles_list = serializers.SerializerMethodField("get_roles_list")
    author_nickname = serializers.SerializerMethodField("get_author_nickname")
    like_count = serializers.SerializerMethodField("get_like_count")

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_like_count(self, obj):
        like_count = Like.objects.filter(post=obj).count()
        return like_count

    def get_skills_list(self, obj):
        skills_queryset = Skill.objects.filter(post=obj)
        skills_list = [skill.name for skill in skills_queryset]
        return skills_list

    def get_roles_list(self, obj):
        roles_queryset = Role.objects.filter(post=obj)
        roles_list = [role.name for role in roles_queryset]
        return roles_list


class PostSerializer(PostSerializerBase):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_nickname",
            "schedule",
            "deadline",
            "roles_list",
            "skills_list",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
            "views",
        ]


class PostDetailSerializer(PostSerializerBase):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_nickname",
            "schedule",
            "deadline",
            "roles_list",
            "skills_list",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
            "comment_set",
            "comment_count",
            "views",
        ]

    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source="comment_set.count", read_only=True)
