from rest_framework import serializers


class SemaphoreSerializer(serializers.Serializer):
    red = serializers.BooleanField(required=False)
    yellow = serializers.BooleanField(required=False)
    green = serializers.BooleanField(required=False)

    def validate(self, attrs):
        return attrs
