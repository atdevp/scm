from rest_framework import serializers
from .models import ApplicationModel


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationModel
        fields = '__all__'


