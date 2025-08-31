from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User

# Import SimpleJWT classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer

# -------------------------------
# Register
# -------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Registration successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "profile": {
                        "bio": user.profile.bio
                    }
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "message": "Registration failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# Profile
# -------------------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# -------------------------------
# Custom JWT Login
# -------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here if needed
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response({
                "message": "Login successful",
                "access": serializer.validated_data['access'],
                "refresh": serializer.validated_data['refresh']
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "message": "Login failed",
                "errors": serializer.errors
            }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the refresh token from the request body
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({"message": "Refresh token required"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()  # blacklist the token
        return Response({"message": "Logout successful"}, status=200)
    except Exception as e:
        return Response({"message": "Logout failed", "error": str(e)}, status=400)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    if target_user == request.user:
        return Response({"message": "You cannot follow yourself"}, status=400)
    
    request.user.profile.following.add(target_user.profile)
    return Response({"message": f"You are now following {target_user.username}"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    if target_user == request.user:
        return Response({"message": "You cannot unfollow yourself"}, status=400)
    
    request.user.profile.following.remove(target_user.profile)
    return Response({"message": f"You have unfollowed {target_user.username}"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_followers(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    followers = target_user.profile.followers.all()
    follower_data = [{"id": f.user.id, "username": f.user.username} for f in followers]
    return Response({"followers": follower_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_following(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    following = target_user.profile.following.all()
    following_data = [{"id": f.user.id, "username": f.user.username} for f in following]
    return Response({"following": following_data})


from rest_framework.decorators import api_view
from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    search_query = request.GET.get('search', '')
    users = User.objects.filter(
        Q(username__icontains=search_query) |
        Q(email__icontains=search_query)
    ).exclude(id=request.user.id)
    
    users_data = [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    return Response({"users": users_data})
