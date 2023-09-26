from rest_framework import serializers
from .models import *

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['name']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ContentItemSerializer(serializers.ModelSerializer):
    categories = CategorieSerializer(many=True, allow_null=True, default=None)
    user = UserSerializer()
    class Meta:
        model = ContentItem
        fields = '__all__'

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()