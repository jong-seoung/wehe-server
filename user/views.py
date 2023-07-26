from django.conf import settings
from rest_framework.views import APIView
from .serializers import LogoutSerializer
from rest_framework.response import Response


class Constants:
    BASE_URL = getattr(settings, "BASE_URL")

    GOOGLE_CALLBACK_URI = f"{BASE_URL}api/v1/user/google/callback/"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(
        [
            "https://www.googleapis.com/auth/userinfo.email",
        ]
    )

    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_CALLBACK_URI = f"{BASE_URL}api/v1/user/kakao/callback/"

    GITHUB_CALLBACK_URI = f"{BASE_URL}api/v1/user/github/callback/"
    GITHUB_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GITHUB_SECRET")


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(message)
