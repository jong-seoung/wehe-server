from django.shortcuts import redirect
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from drf_yasg.utils import swagger_auto_schema
import requests
from user.models import User
from .serializers import TokenResponseSerializer
from rest_framework.response import Response
from .views import Constants


class GithubLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="깃허브 로그인")
    def get(self, request):
        return redirect(
            f"https://github.com/login/oauth/authorize?client_id={Constants.GITHUB_CLIENT_ID}"
            f"&redirect_uri={Constants.GITHUB_CALLBACK_URI}"
        )


class GithubCallbackView(APIView):
    permission_classes = [AllowAny]
    schema = None

    @swagger_auto_schema(operation_id="깃허브 로그인 콜백")
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        GITHUB_CLIENT_ID = Constants.GITHUB_CLIENT_ID
        GITHUB_CLIENT_SECRET = Constants.GITHUB_CLIENT_SECRET
        GITHUB_CALLBACK_URI = Constants.GITHUB_CALLBACK_URI
        code = request.GET.get("code")

        token_req = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={GITHUB_CLIENT_ID}"
            f"&client_secret={GITHUB_CLIENT_SECRET}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}"
            f"&response_type=code",
            headers={"Accept": "application/json"},
        )
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get("error") == "invalid_request":
                return redirect(f"{BASE_URL}api/v1/user/google/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")
        user_req = requests.get(
            f"https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_json = user_req.json()
        error = user_json.get("error")
        if error is not None:
            return redirect(f"{BASE_URL}api/v1/user/google/login")
        email = user_json.get("email")
        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return JsonResponse(
                    {"err_msg": "email exists but not social user"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if social_user.provider != "github":
                return JsonResponse(
                    {"err_msg": "no matching social type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data = {"access_token": access_token, "code": code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/github/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signin"}, status=accept_status
                )
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res
        except User.DoesNotExist:
            data = {"access_token": access_token, "code": code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/github/login/finish/", data=data
            )
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse(
                    {"err_msg": "failed to signup"}, status=accept_status
                )
            user = User.objects.get(email=email)
            serializer = TokenResponseSerializer(user)
            data = serializer.to_representation(serializer)
            res = Response(
                data,
                status=status.HTTP_200_OK,
            )
            return res


class GithubLoginToDjango(SocialLoginView):
    permission_classes = [AllowAny]
    schema = None

    adapter_class = github_view.GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = Constants.GITHUB_CALLBACK_URI
