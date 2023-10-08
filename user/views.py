from django.conf import settings
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from user.serializers import LogoutSerializer, UserInfoSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import User
from user.permissions import IsOwnerOrReadOnly


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
    KAKAO_CALLBACK_URI = f"http://localhost:3000/kakao"

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


class UserInfoAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
