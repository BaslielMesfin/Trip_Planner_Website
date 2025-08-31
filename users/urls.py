from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, ProfileView, CustomTokenObtainPairView, logout_view
from .views import (
    follow_user, unfollow_user,
    list_followers, list_following, list_users
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # custom login
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),           # get/update current user
    path('logout/', logout_view, name='logout'),
    # Social features
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    path('followers/<int:user_id>/', list_followers, name='list-followers'),
    path('following/<int:user_id>/', list_following, name='list-following'),
    path('users/', list_users, name='list-users'),
]
