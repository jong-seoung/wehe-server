from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from posts.models import Post, Like
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import (
    PostSerializer,
    PostDetailSerializer,
    PopularPostSerializer,
)
from user.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PostListAPI(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "page",
                in_=openapi.IN_QUERY,
                description="페이지 번호",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        page = request.GET.get("page")
        paginator = Paginator(self.queryset, 16)
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            page_obj = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            page_obj = paginator.page(page)

        page_obj = page_obj.object_list
        self.queryset = page_obj

        return self.list(request, *args, **kwargs)


class PostCreateAPI(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'post_id'
    allowed_methods = ["GET", "DELETE", "PATCH"]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=pk)
        session_key = f"post_viewed_{pk}"

        if not request.session.get(session_key, False):
            post.views += 1
            post.save()
            request.session[session_key] = True
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=pk)

        self.check_object_permissions(request, post)

        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(request, post)

        post.delete()

        return Response({"message": "Object deleted successfully."})


class PostLikeAPI(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        email = request.user
        user = User.objects.get(email=email)
        try:
            like = Like.objects.get(user_id=user.id, post_id=post.id)
            like.delete()
            is_liked = False
        except Like.DoesNotExist:
            Like.objects.create(user_id=user.id, post_id=post.id)
            is_liked = True
        return Response({"is_liked": is_liked})


class PopularPostAPI(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-score")[:4:]
    serializer_class = PopularPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
