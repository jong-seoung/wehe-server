from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from posts.models import Post, Like
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import PostSerializer, PostDetailSerializer, PopularPostSerializer
from user.models import User


class PostAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        post = get_object_or_404(Post, pk=pk)
        session_key = f"post_viewed_{pk}"

        if not request.session.get(session_key, False):
            post.views += 1
            post.save()
            request.session[session_key] = True
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class PostLikeAPI(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
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
    queryset = Post.objects.all().order_by('-score')[:4:]
    serializer_class = PopularPostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
