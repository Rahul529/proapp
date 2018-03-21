from django.shortcuts import render
from django.contrib.auth.models import User 
from rest_framework import permissions
from rest_framework import routers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from proapp.serializers import UserSerializer, AuthSerializer
import uuid
import json
from rest_framework.authtoken.models import Token


class Userlist(APIView):
    ''' Returns the all the users  
    '''
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
    
    def get(self, request, format=None):
            users = User.objects.all()
            users_data = UserSerializer(users)
            users_data = users_data.get_data(users)
            return Response(users_data)


class UserCreate(APIView):
    ''' Post: acpets json user details
    '''
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format=None):
        user_data = json.loads(request.body.decode('utf-8'))
        user_create = UserSerializer(data=user_data)
        if user_create.is_valid():
            user_create.create(user_create.validated_data)
            msg = {'message': 'success', 'status': 1}
            return Response(json.dumps(msg), status =201)
        else:
            msg = {'message': 'User not created' , 'status': 0}
            return Response(json.dumps(msg), status=400)


class AuthUser(APIView):
    ''' Authenticates the user params: username, password in json
        returns the token in json
    '''
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            user_data = json.loads(request.body.decode('utf-8'))
            auth_user = AuthSerializer(data=user_data)
            if auth_user.is_valid():
                user = User.objects.get(username=user_data['username'],
                                        password=user_data['password'])
                token, created = Token.objects.get_or_create(user=user)
                data = {'token': token.key}
                return Response(data, status=200)
            else:
                msg = {'message': 'username '}
                return Response(msg, status=400)
        except User.DoesNotExist:
            msg = {'message': 'user doesnot exists'}
            return Response(msg, status=400)
        except ValueError:
            msg = {'message': 'Bad Request or data'}
            return Response(msg, status=400)


class LogoutUser(APIView):
    ''' logs outthe user
    '''
    permissions_classes = [permissions.IsAuthenticated]

    def get(self,request, format=None):
        if request.user.is_active:
            token = Token.objects.get(user=request.user)
            token.delete()
            msg = {'message': 'successfully logged out.'}
            return Response(msg, status=200)
