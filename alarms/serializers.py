import json
from django_eventstream.models import Event
from rest_framework import serializers

class EventSerializers(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "channel",
            "type",
            "data",
            "eid",
            "created",
        ]

    data = serializers.SerializerMethodField("get_data")
    created = serializers.SerializerMethodField("get_created")

    def get_data(self, obj):
        try:
            data = json.loads(obj.data)
        except json.JSONDecodeError:
            data = {}
        return data

    def get_created(self, obj):
        date_format = "%Y-%m-%d %H:%M"
        created = obj.created.strftime(date_format)
        return created
