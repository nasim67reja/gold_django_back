from rest_framework import serializers
from .models import PriceData
from datetime import datetime

class UnixTimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            # Convert unix timestamp → datetime
            return datetime.fromtimestamp(float(value))
        except Exception:
            self.fail("invalid", format="unix timestamp")

    def to_representation(self, value):
        # Convert datetime → unix timestamp for response
        return int(value.timestamp())


class PriceDataSerializer(serializers.ModelSerializer):
    time = UnixTimestampField()

    class Meta:
        model = PriceData
        fields = "__all__"
