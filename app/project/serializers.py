from rest_framework import serializers
from .models import ProjectModel, PackageLogModel


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = '__all__'


class PackageLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageLogModel
        fields = '__all__'