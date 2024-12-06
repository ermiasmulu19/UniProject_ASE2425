from rest_framework import serializers

from .models import Duck


class DuckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duck
        fields = '__all__'