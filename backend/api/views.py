from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PersonSerializer , UserSerializer
from .models import Person
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import logging
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def hello_world(request):
    if request.method == "GET":
        person = {
            "name": "Anwar",
            "age": 22
        }
        return Response(person)
    elif request.method == "POST":
        person = {
            "name": "mUSTHAFA",
            "age": 22
        }
        return Response(person)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person(request):
    if request.method == "GET":
        objPerson = Person.objects.all()
        serializer = PersonSerializer(objPerson, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_detail(request, pk):
    obj = get_object_or_404(Person, pk=pk)

    if request.method == 'GET':
        serializer = PersonSerializer(obj)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = PersonSerializer(obj, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)
            else:
                return Response({"message": "Invalid username or password"}, status=400)
        except Exception as e:
            return Response({"message": "Internal server error"}, status=500)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def signout(request):
    try:
        token = request.auth
        if token:
            token.delete()
            return Response({"message": "User signed out successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid token or user not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)