import requests
from django.conf import settings
from rest_framework.views import APIView
from user.serializers import LogoutSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    GOOGLE_CALLBACK_URI = f"http://localhost:3000/google"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(
        [
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )

    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"http://localhost:3000/kakao"

    GITHUB_CALLBACK_URI = f"http://localhost:3000/github"
    GITHUB_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GITHUB_SECRET")


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['refresh']
        ),
        responses={400: 'Bad Request'},  # 응답 코드 및 설명
    )
    def post(self, request):
        refresh_token = request.query_params.get('refresh')
        print(refresh_token)
        data = {'refresh': refresh_token}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(message)
