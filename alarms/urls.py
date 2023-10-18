from django.urls import path, include
import django_eventstream
from . import views


urlpatterns = [
        path('events/', views.AlarmList.as_view()),
        path('events/<user_id>/', include(django_eventstream.urls), {
            'format-channels': ['user-{user_id}']
        }),
]