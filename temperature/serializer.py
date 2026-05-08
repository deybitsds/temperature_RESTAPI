from rest_framework import serializers


class TemperatureSerializer(serializers.Serializer):

    temperature = serializers.FloatField(required=False)
    humidity = serializers.FloatField(required=False)
    heat_index = serializers.FloatField(required=False)

    token = serializers.CharField(required=False, max_length=100)

    def validate(self, attrs):
        temperature = attrs.get('temperature')
        humidity = attrs.get('humidity')
        heat_index = attrs.get('heat_index')
        return attrs
