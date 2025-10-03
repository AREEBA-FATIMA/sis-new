from rest_framework import serializers
from .models import Principal

class PrincipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Principal
        fields = "__all__"
