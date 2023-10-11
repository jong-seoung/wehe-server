from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from user.models import User, Skill, Role, UserImage
from user.serializers import UserInfoSerializer


class UserInfoAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    user_instance = None

    def get_user_instance(self):
        auth_header = self.request.headers.get('Authorization')
        access_tokne = auth_header.split(' ')[1]
        decoded = AccessToken(access_tokne)
        user_id = decoded['user_id']
        self.user_instance = User.objects.get(id=user_id)
        return self.user_instance

    @swagger_auto_schema(security=[{"Bearer": []}])
    def get_object(self):
        user = self.get_user_instance()
        return user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING,description='name'),
            'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='User nickname (max length: 15).'),
            'birthday': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, description='User birthday, format (e.g., "1990-01-01").'),
            'skills_list': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='List of user skills.'),
            'roles_list': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description='List of user roles.'),
            'profile_img': openapi.Schema(type=openapi.TYPE_STRING, description='URL to user profile image.'),
        }
    ))
    def patch(self, request, *args, **kwargs):
        user = self.get_user_instance()

        updated_at = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        nickname =request.data.get('nickname')
        name = request.data.get('name')
        birthday =request.data.get('birthday')

        skills_list = request.data.get('skills_list')
        roles_list = request.data.get('roles_list')

        profile_img =request.data.get('profile_img')

        validated_skills = []
        for skill_name in skills_list:
            skill = Skill.objects.filter(name=skill_name).first()
            if skill:
                validated_skills.append(skill)
        user.skills.set(validated_skills)

        validated_roles = []
        for role_name in roles_list:
            role = Role.objects.filter(name=role_name).first()
            if roles_list:
                validated_roles.append(role)
        user.roles.set(validated_roles)

        if profile_img:
            new_profile_image = UserImage.objects.create(image=profile_img)
            user.user_image = new_profile_image

        user.updated_at = updated_at
        user.nickname = nickname
        user.name = name
        user.birthday = birthday

        user.save()

        return self.partial_update(request, *args, **kwargs)