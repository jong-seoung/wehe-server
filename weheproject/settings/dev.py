from .base import *
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg)


DEBUG = False

ALLOWED_HOSTS = ["*"]

BASE_URL = get_env_variable("BASE_URL")

SECRET_KEY = get_env_variable("DJANGO_SECRET")
STATE = get_env_variable("STATE")
KAKAO_REST_API_KEY = get_env_variable("KAKAO_REST_API_KEY")
SOCIAL_AUTH_GITHUB_CLIENT_ID = get_env_variable("SOCIAL_AUTH_GITHUB_CLIENT_ID")
SOCIAL_AUTH_GITHUB_SECRET = get_env_variable("SOCIAL_AUTH_GITHUB_SECRET")
SOCIAL_AUTH_GOOGLE_CLIENT_ID = get_env_variable("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_SECRET = get_env_variable("SOCIAL_AUTH_GOOGLE_SECRET")


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

SIMPLE_JWT = {
    "JWT_SECRET_KEY": SECRET_KEY,
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "TOKEN_OBTAIN_SERIALIZER": "user.serializers.MyTokenObtainPairSerializer",
}

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS = ("https://port-0-wehe-k19y2kljve3tgo.sel4.cloudtype.app",)
CSRF_TRUSTED_ORIGINS = ("https://*", "http://*",)
