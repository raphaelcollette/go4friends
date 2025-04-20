from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='60/m', block=True)
def me(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "bio": user.bio,
        "location": user.location,
        "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None,
    }
    return Response(data)


@api_view(['POST'])
@ratelimit(key='ip', rate='5/m', block=True)
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

    hashed_password = make_password(password)

    user = User.objects.create(
        username=username,
        email=email,
        password=hashed_password
    )

    return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)

class MyTokenObtainPairView(TokenObtainPairView):
    
    @method_decorator(ratelimit(key='ip', rate='10/m', block=True)) 
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='30/m', block=True)
def update_me(request):
    user = request.user

    # Allow JSON and form uploads
    parser_classes = [MultiPartParser, FormParser]

    full_name = request.data.get('full_name')
    bio = request.data.get('bio')
    location = request.data.get('location')
    profile_picture = request.FILES.get('profile_picture')

    if full_name is not None:
        user.full_name = full_name
    if bio is not None:
        user.bio = bio
    if location is not None:
        user.location = location
    if profile_picture is not None:
        user.profile_picture = profile_picture

    user.save()

    return Response({"message": "Profile updated successfully!"})

