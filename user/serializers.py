from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from user.models import User, UserImage
from skills.serializers import SkillSerializer
from roles.serializers import RoleSerializer


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['image']


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
            message = True
        else:
            message = False

        return {
            "message": message,
            "token": {
                "email": self.user.email,
                "access": self.get_access_token(),
                "refresh": self.get_refresh_token(),
            },
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        if not self.token:
            raise serializers.ValidationError('Token is required.')
        return attrs

    def save(self, **kwargs):
        try:
            refresh_token = RefreshToken(self.token)
            refresh_token.blacklist()
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

    skills_list = SkillSerializer(many=True)
    roles_list = RoleSerializer(many=True)
    profile_img = serializers.SerializerMethodField("get_profile_img")

    def get_profile_img(self, obj):
        profile_img = UserImage.objects.get(id=obj.user_image_id)
        return profile_img.image.url
