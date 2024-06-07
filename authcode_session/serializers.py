# api/serializers.py
from rest_framework import serializers


class SerialValidationSerializer(serializers.Serializer):
    serial = serializers.CharField(max_length=200)


class SessionValidationSerializer(serializers.Serializer):
    session_id = serializers.CharField()
