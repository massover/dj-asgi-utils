from rest_framework import serializers

from .models import Toast


class ToastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Toast
        fields = ["id", "message"]
