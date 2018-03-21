from rest_framework import serializers
from rest_framework.serializers import Serializer,ModelSerializer
from django.contrib.auth.models import User 


class CommentSerializer(Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


class UserSerializer(ModelSerializer):
    username = serializers.CharField(min_length=6, required=True)
    password = serializers.CharField(min_length=6, required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','password']
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)


    def get_data(self, data):
        users = []
        for x in data:
            user = {}
            user['username'] = x.username
            user['email'] = x.email
            user['id'] = x.id
            user['password'] = x.password
            users.append(user)
        return users

    def validate_data(self):
        if len(self.data['username']) < 6:
            raise serializers.ValidationError(
                   'username must not be atleast 6 characters')
        return self.data



class AuthSerializer(Serializer):
    username = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)