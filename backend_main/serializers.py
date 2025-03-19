from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = ['id', 'username', 'password', 'user_role', 'email']
        extra_kwargs = {
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



class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessObject
        fields = '__all__'
    

        
class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnapshotObject
        fields = '__all__'