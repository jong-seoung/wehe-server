from .base import *
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


ALLOWED_HOSTS = ["*"]

SECRET_KEY = get_env_variable("DJANGO_SECRET")
STATE = get_env_variable("STATE")
KAKAO_REST_API_KEY = get_env_variable("KAKAO_REST_API_KEY")
SOCIAL_AUTH_GITHUB_CLIENT_ID = get_env_variable("SOCIAL_AUTH_GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = get_env_variable("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GOOGLE_CLIENT_ID = get_env_variable("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_SECRET = get_env_variable("SOCIAL_AUTH_GOOGLE_SECRET")

DEBUG = False

SIMPLE_JWT = {
    "JWT_SECRET_KEY": SECRET_KEY,
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "TOKEN_OBTAIN_SERIALIZER": "user.serializers.MyTokenObtainPairSerializer",
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("DB_NAME"),
        "USER": get_env_variable("DB_USER"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST"),
        "PORT": get_env_variable("DB_PORT"),
    }
}
