from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):  
    class Meta:
        model = MyUser
        fields = ['username', 'password','email']

    def create(self, validated_data):
        user = MyUser.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20)

class DetailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=20)

class RateSerializer(serializers.Serializer):
    movie = serializers.CharField(max_length=250)
    rate = serializers.IntegerField(default=1,validators=[MaxValueValidator(5), MinValueValidator(1)])