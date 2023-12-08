from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from comments.models import Comment
from posts.permissions import IsOwnerOrReadOnly
from posts.serializers import CommentSerializer
from user.models import User
from posts.models import Post
from django_eventstream import send_event


class CommentCreateAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_user_instance(self):
        auth_header = self.request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        decoded = AccessToken(access_token)
        user_id = decoded['user_id']
        return user_id

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs["post_id"]
        comments = Comment.objects.filter(post_id=post_id)
        self.queryset = comments
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs["post_id"]
        author_id = self.get_user_instance()
        content = request.data.get('content')
        comment = Comment.objects.create(post_id=post_id, author_id=author_id, content=content)
        comment = self.serializer_class(comment)

        user = User.objects.get(id=author_id)
        post = Post.objects.get(id=post_id)
        send_message = f'{user.nickname}님이 댓글을 남겼습니다.\n"{content}"\n{post.title}'

        send_event('user-{}'.format(post.author_id), 'message', send_message, json_encode=False)
        return Response(comment.data)


class CommentDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    allowed_methods = ["DELETE", "PATCH"]

    def get_user_instance(self):
        auth_header = self.request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        decoded = AccessToken(access_token)
        user_id = decoded['user_id']
        return user_id

    def get_object(self):
        post_id = self.kwargs['post_id']
        comment_id = self.kwargs['comment_id']
        author_id = self.get_user_instance()
        return Comment.objects.get(post_id=post_id, id=comment_id, author_id=author_id)