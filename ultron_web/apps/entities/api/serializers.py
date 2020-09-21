from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validate_data):
        user = User(
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name'],
            username=validate_data['username'],
            password=make_password(validate_data['password']),
        )
        
        user.save()
        return user
