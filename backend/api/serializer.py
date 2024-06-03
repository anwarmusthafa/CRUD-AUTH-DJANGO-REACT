from rest_framework import serializers
from .models import Person
from .models import CustomUser
from django.contrib.auth.hashers import make_password
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Use set_password to hash the password
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)


    