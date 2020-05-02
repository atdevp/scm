from rest_framework import serializers
from .models import MenuModel


class MeunSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuModel
        fields = '__all__'
