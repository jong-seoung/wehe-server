from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        pass

    def generate_tokens(self, user):
        access_token = AccessToken.for_user(user)
        access_token['nickname'] = user.nickname
        refresh_token = RefreshToken.for_user(user)

        return {
            'access_token': str(access_token),
            'refresh_token': str(refresh_token),
        }
