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
from .serializers import UserPublicSerializer
from friends.models import FriendRequest
from django.db.models import Q

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='60/m', block=True)
def me(request):
    serializer = UserPublicSerializer(request.user, context={'request': request})
    return Response(serializer.data)


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

    parser_classes = [MultiPartParser, FormParser]

    full_name = request.data.get('full_name')
    bio = request.data.get('bio')
    location = request.data.get('location')
    interests = request.data.get('interests')
    profile_picture = request.FILES.get('profile_picture')
    major = request.data.get('major')
    graduation_year = request.data.get('graduation_year')
    is_private = request.data.get('is_private')

    if full_name is not None:
        user.full_name = full_name
    if bio is not None:
        user.bio = bio
    if location is not None:
        user.location = location
    if profile_picture is not None:
        user.profile_picture = profile_picture
    if major is not None:
        user.major = major
    if graduation_year is not None:
        user.graduation_year = graduation_year    

    if is_private is not None:
        user.is_private = is_private in [True, 'true', 'True', 1, '1']    

    if interests is not None:
        if isinstance(interests, list):
            user.interests = interests
        else:
            try:
                user.interests = json.loads(interests)
            except Exception:
                return Response({"error": "Invalid interests format."}, status=status.HTTP_400_BAD_REQUEST)

    user.save()
    return Response({"message": "Profile updated successfully!"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)[:10]
        serializer = UserPublicSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    return Response([])

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username=username)

        # Allow viewing if you're the owner
        if request.user == user:
            serializer = UserPublicSerializer(user, context={'request': request})
            return Response(serializer.data)

        # If profile is private, check if viewer is a friend
        if user.is_private:
            is_friend = FriendRequest.objects.filter(
                Q(from_user=request.user, to_user=user) |
                Q(from_user=user, to_user=request.user),
                status='accepted'
            ).exists()

            if not is_friend:
                return Response({"error": "This profile is private."}, status=status.HTTP_403_FORBIDDEN)

        # Otherwise, allow viewing
        serializer = UserPublicSerializer(user, context={'request': request})
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='10/m', block=True)
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 8:
        return Response({"error": "New password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@ratelimit(key='ip', rate='5/m', block=True)
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)