from rest_framework import serializers
from .models import PriceData
from datetime import datetime
from django.utils import timezone


class UnixTimestampField(serializers.DateTimeField):
    def to_internal_value(self, value):
        try:
            # Convert unix timestamp → UTC-aware datetime
            dt = datetime.fromtimestamp(float(value), tz=timezone.utc)
            return dt
        except Exception:
            self.fail("invalid", format="unix timestamp")

    def to_representation(self, value):
        # Always return unix timestamp
        return int(value.timestamp())


class PriceDataSerializer(serializers.ModelSerializer):
    time = UnixTimestampField()

    class Meta:
        model = PriceData
        fields = "__all__"
