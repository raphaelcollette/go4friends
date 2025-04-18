from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password

@api_view(['GET', 'POST'])
def users_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_data = [{"username": user.username, "email": user.email} for user in users]
        return Response(users_data)

    elif request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')

        if not username or not email:
            return Response({"error": "Username and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(username=username, email=email)
        return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)
    user = User.objects.create(username=username, email=email, password=hashed_password)

    return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)