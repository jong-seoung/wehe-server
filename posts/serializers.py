from posts.models import Post, Like
from skills.models import Skill
from roles.models import Role
from rest_framework import serializers
from comments.serializers import CommentSerializer


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PostSerializerBase(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    roles = RoleSerializer(many=True)
    author_nickname = serializers.SerializerMethodField("get_author_nickname")
    like_count = serializers.SerializerMethodField("get_like_count")

    def get_author_nickname(self, obj):
        return obj.author.nickname

    def get_like_count(self, obj):
        like_count = Like.objects.filter(post=obj).count()
        return like_count


class PostSerializer(PostSerializerBase):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_nickname",
            "schedule",
            "deadline",
            "roles",
            "skills",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
            "views",
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user

        roles_data = validated_data.pop('roles', [])
        skills_data = validated_data.pop('skills', [])

        post = Post.objects.create(**validated_data)

        for i in range(len(roles_data)):
            role_name = roles_data[i]['name']
            role_instance, created = Role.objects.get_or_create(name=role_name)
            post.roles.add(role_instance)

        for i in range(len(skills_data)):
            skill_name = skills_data[i]['name']
            skill_instance, created = Skill.objects.get_or_create(name=skill_name)
            post.skills.add(skill_instance)

        return post


class PostDetailSerializer(PostSerializerBase):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_nickname",
            "schedule",
            "deadline",
            "roles",
            "skills",
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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.schedule = validated_data.get('schedule', instance.schedule)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.contact_url = validated_data.get('contact_url', instance.contact_url)
        instance.is_private = validated_data.get('is_private', instance.is_private)

        instance.save()
        instance.roles.clear()
        instance.skills.clear()

        roles_data = validated_data.get('roles', [])
        skills_data = validated_data.get('skills', [])

        for i in range(len(roles_data)):
            role_name = roles_data[i]['name']
            role_instance, created = Role.objects.get_or_create(name=role_name)
            instance.roles.add(role_instance)

        for i in range(len(skills_data)):
            skill_name = skills_data[i]['name']
            skill_instance, created = Skill.objects.get_or_create(name=skill_name)
            instance.skills.add(skill_instance)

        return instance

class PopularPostSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_nickname",
            "schedule",
            "deadline",
            "roles",
            "skills",
            "contact",
            "contact_url",
            "is_private",
            "created_at",
            "updated_at",
            "like_count",
            "views",
        ]