from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_object
        fields = ['id', 'username', 'password', 'user_role']
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'id': {'read_only': True},
        }
        
    def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
            instance.save()
            return instance
