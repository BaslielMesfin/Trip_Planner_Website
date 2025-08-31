from django.urls import path
from .views import (
    TripListCreateView, TripDetailView,
    ToDoListCreateView, ToDoDetailView
)
from .views import mark_trip_complete, photos_view, delete_photo, add_favorite_moment, view_user_trips

urlpatterns = [
    path('trips/', TripListCreateView.as_view(), name='trips-list-create'),
    path('trips/<int:pk>/', TripDetailView.as_view(), name='trips-detail'),

    # To-Do items
    path('trips/<int:trip_id>/todos/', ToDoListCreateView.as_view(), name='todos-list-create'),
    path('todos/<int:pk>/', ToDoDetailView.as_view(), name='todos-detail'),

    # Mark trip complete
    path('trips/<int:trip_id>/mark-complete/', mark_trip_complete, name='mark-trip-complete'),

    # Photos
    path('trips/<int:trip_id>/photos/', photos_view, name='trip-photos'),
    path('photos/<int:photo_id>/', delete_photo, name='delete-photo'),

    # Favorite Moments
    path('trips/<int:trip_id>/favorite_moments/', add_favorite_moment, name='add-favorite-moment'),

    # View user's completed trips
    path('users/<int:user_id>/trips/', view_user_trips, name='view-user-trips'),

]

