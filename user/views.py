from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class KakaoLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("카카오 페이지")


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("구글 페이지")


class GithubLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response("깃허브 페이지")


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response()
