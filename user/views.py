from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings
import requests
from rest_framework import status
from django.shortcuts import redirect
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from user.models import User
from user.serializer import JWTTokenSerializer
from rest_framework.response import Response


class GenerateJWTTokenView(APIView):
    def post(self, request):
        user = request.user
        serializer = JWTTokenSerializer()
        tokens = serializer.generate_tokens(user)

        access_token = tokens['access_token']
        refresh_token = tokens['refresh_token']

        return Response({'access_token': access_token, 'refresh_token': refresh_token})


class Constants:
    BASE_URL = 'http://127.0.0.1:8000/'

    GOOGLE_CALLBACK_URI = f"{BASE_URL}api/v1/user/google/callback/"
    GOOGLE_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    GOOGLE_SCOPE = " ".join(["https://www.googleapis.com/auth/userinfo.email", ])

    REST_API_KEY = getattr(settings, 'KAKAO_REST_API_KEY')
    KAKAO_CALLBACK_URI = f"{BASE_URL}api/v1/user/kakao/callback/"

    GITHUB_CALLBACK_URI = f"{BASE_URL}api/v1/user/github/callback/"
    GITHUB_CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GITHUB_SECRET")


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="구글 로그인")
    def get(self, request):
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={Constants.GOOGLE_CLIENT_ID}"
                        f"&response_type=code&redirect_uri={Constants.GOOGLE_CALLBACK_URI}&scope={Constants.GOOGLE_SCOPE}")


class GoogleCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="구글 로그인 콜백")
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        GOOGLE_CLIENT_ID = Constants.GOOGLE_CLIENT_ID
        GOOGLE_CLIENT_SECRET = Constants.GOOGLE_CLIENT_SECRET
        GOOGLE_CALLBACK_URI = Constants.GOOGLE_CALLBACK_URI
        code = request.GET.get('code')

        data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_CALLBACK_URI,
            'grant_type': 'authorization_code'
        }
        token_req = requests.post("https://oauth2.googleapis.com/token", data=data)
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get('error') == 'invalid_request':
                return redirect(f"{BASE_URL}api/v1/user/google/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get('access_token')

        email_req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/userinfo", params={'alt': 'json', 'access_token': access_token})
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return JsonResponse({'error': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
        email_req_json = email_req.json()
        email = email_req_json.get('email')
        if not email:
            return JsonResponse({'error': 'email not found'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            social_user = SocialAccount.objects.get(user=user)

            if social_user.provider != 'google':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            data = {'access_token': access_token, 'code': code}

            accept = requests.post(f"{BASE_URL}api/v1/user/google/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin1'}, status=accept_status)

            accept_json = accept.json()
            accept_json.pop('user', None)
            return redirect(settings.LOGIN_REDIRECT_URL)

        except User.DoesNotExist:
            data = {'app': GOOGLE_CLIENT_ID, 'token': access_token, 'code': code}
            accept = requests.post(f"{BASE_URL}api/v1/user/google/login/finish/", data=data)
            accept_status = accept.status_code

            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)

            accept_json = accept.json()
            accept_json.pop('user', None)
            return JsonResponse(accept_json)

        except (User.DoesNotExist, SocialAccount.DoesNotExist):
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginToDjango(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = Constants.GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


class KakaoLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="카카오 로그인")
    def get(self, request):
        return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={Constants.REST_API_KEY}"
                        f"&redirect_uri={Constants.KAKAO_CALLBACK_URI}&response_type=code")


class KakaoCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="카카오 로그인 콜백")
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        REST_API_KEY = Constants.REST_API_KEY
        KAKAO_CALLBACK_URI = Constants.KAKAO_CALLBACK_URI
        code = request.GET.get("code")
        """
            Access Token Request
        """
        token_req = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}"
            f"&redirect_uri={KAKAO_CALLBACK_URI}&code={code}")
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get('error') == 'invalid_request':
                return redirect(f"{BASE_URL}api/v1/user/kakao/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get("access_token")
        id_token = token_req_json.get("id_token")

        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get('kakao_account')
        email = kakao_account.get('email')
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        try:
            if social_user is None:
                return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'kakao':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            jwt_token_view = GenerateJWTTokenView()
            jwt_token = jwt_token_view.post(request).data['access_token']
            request.session['jwt_token'] = jwt_token
            data = {'access_token': access_token, 'code': code, 'id_token': id_token}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/kakao/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()
            accept_json.pop('user', None)
            return redirect(settings.LOGIN_REDIRECT_URL)
        except User.DoesNotExist:
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/kakao/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            jwt_token_view = GenerateJWTTokenView()
            jwt_token = jwt_token_view.post(request).data['access_token']
            request.session['jwt_token'] = jwt_token
            accept_json = accept.json()
            accept_json.pop('user', None)
            return redirect(settings.LOGIN_REDIRECT_URL)


class KakaoLoginToDjango(SocialLoginView):
    permission_classes = [AllowAny]

    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = Constants.KAKAO_CALLBACK_URI


class GithubLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="깃허브 로그인")
    def get(self, request):
        return redirect(f"https://github.com/login/oauth/authorize?client_id={Constants.GITHUB_CLIENT_ID}"
                        f"&redirect_uri={Constants.GITHUB_CALLBACK_URI}")


class GithubCallbackView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_id="깃허브 로그인 콜백")
    def get(self, request):
        BASE_URL = Constants.BASE_URL
        GITHUB_CLIENT_ID = Constants.GITHUB_CLIENT_ID
        GITHUB_CLIENT_SECRET = Constants.GITHUB_CLIENT_SECRET
        GITHUB_CALLBACK_URI = Constants.GITHUB_CALLBACK_URI
        code = request.GET.get('code')

        token_req = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={GITHUB_CLIENT_ID}"
            f"&client_secret={GITHUB_CLIENT_SECRET}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}"
            f"&response_type=code", headers={'Accept': 'application/json'})
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            if token_req_json.get('error') == 'invalid_request':
                return redirect(f"{BASE_URL}api/v1/user/google/login")
            return JsonResponse(token_req_json)
        access_token = token_req_json.get('access_token')
        user_req = requests.get(f"https://api.github.com/user",
                                headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_req.json()
        error = user_json.get("error")
        if error is not None:
            return redirect(f"{BASE_URL}api/v1/user/google/login")
        email = user_json.get("email")
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        try:
            if social_user is None:
                return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'github':
                return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            jwt_token_view = GenerateJWTTokenView()
            jwt_token = jwt_token_view.post(request).data['access_token']
            request.session['jwt_token'] = jwt_token
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/github/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signin'}, status=accept_status)
            accept_json = accept.json()
            accept_json.pop('user', None)
            return redirect(settings.LOGIN_REDIRECT_URL)
        except User.DoesNotExist:
            data = {'access_token': access_token, 'code': code}
            accept = requests.post(
                f"{BASE_URL}api/v1/user/github/login/finish/", data=data)
            accept_status = accept.status_code
            if accept_status != 200:
                return JsonResponse({'err_msg': 'failed to signup'}, status=accept_status)
            jwt_token_view = GenerateJWTTokenView()
            jwt_token = jwt_token_view.post(request).data['access_token']
            request.session['jwt_token'] = jwt_token
            accept_json = accept.json()
            accept_json.pop('user', None)
            return redirect(settings.LOGIN_REDIRECT_URL)


class GithubLoginToDjango(SocialLoginView):
    permission_classes = [AllowAny]

    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = Constants.GITHUB_CALLBACK_URI
    client_class = OAuth2Client
