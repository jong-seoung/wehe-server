from __future__ import unicode_literals
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import ListAPIView
from django_eventstream.models import Event
from alarms.serializers import EventSerializers


class AlarmList(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_user_instance(self, request, *args, **kwargs):
        auth_header = self.request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        decoded = AccessToken(access_token)
        user_id = decoded['user_id']
        return user_id

    def get(self, request, *args, **kwargs):
        user_id = self.get_user_instance(self.request)
        try:
            room = Event.objects.filter(channel='user-{}'.format(user_id)).order_by('-created')[:10]
            self.queryset = room
        except Event.DoesNotExist:
            print(1234)

        return self.list(request, *args, **kwargs)