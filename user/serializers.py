from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user.models import User, UserImage
from skills.models import Skill
from roles.models import Role


class TokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = TokenObtainPairSerializer.get_token(user)
        self.user = user

    def get_access_token(self):
        return str(self.token.access_token)

    def get_refresh_token(self):
        return str(self.token)

    def to_representation(self, instance):
        nickname = self.user.nickname
        if nickname is None:
            message = "first login"
        else:
            message = "not first login"

        return {
            "message": message,
            "token": {
                "access": self.get_access_token(),
                "refresh": self.get_refresh_token(),
            },
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

            return {"message": "logout success"}

        except TokenError:
            return {"message": "bad_token"}


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "created_at",
            "updated_at",
            "email",
            "name",
            "nickname",
            "birthday",
            "user_image",
            "profile_img",
            "skills_list",
            "roles_list",
        ]

    skills_list = serializers.SerializerMethodField("get_skills_list")
    roles_list = serializers.SerializerMethodField("get_roles_list")
    profile_img = serializers.SerializerMethodField("get_profile_img")

    def get_profile_img(self, obj):
        profile_img = UserImage.objects.get(id=obj.user_image_id)
        return profile_img.image.url

    def get_skills_list(self, obj):
        skills_queryset = Skill.objects.filter(user=obj)
        skills_list = [skill.name for skill in skills_queryset]
        return skills_list

    def get_roles_list(self, obj):
        roles_queryset = Role.objects.filter(post=obj.id)
        roles_list = [role.name for role in roles_queryset]
        return roles_list
