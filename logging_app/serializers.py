from logging_app.models import Users,Session,Events
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer

class UsersSerializer(DocumentSerializer):
    username = serializers.CharField(read_only=False)
    class Meta:
        model = Users
        fields = '__all__'

class SessionSerializer(DocumentSerializer):
    id = serializers.CharField(read_only=False)
    username = UsersSerializer()
    class Meta:
        model = Session
        fields = '__all__'

class EventsSerializer(DocumentSerializer):
    username = UsersSerializer()
    sessionId = SessionSerializer()
    class Meta:
        model = Events
        fields = '__all__'