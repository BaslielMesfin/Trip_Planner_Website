from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Trip, ToDoItem, Photo, FavoriteMoment
from .serializers import TripSerializer, ToDoItemSerializer, PhotoSerializer, FavoriteMomentSerializer
from django.contrib.auth.models import User

# -------------------------------
# Trips
# -------------------------------
class TripListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user)

# -------------------------------
# ToDoItems
# -------------------------------
class ToDoListCreateView(generics.ListCreateAPIView):
    serializer_class = ToDoItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return ToDoItem.objects.filter(trip__id=trip_id, trip__user=self.request.user)

    def perform_create(self, serializer):
        trip_id = self.kwargs['trip_id']
        trip = Trip.objects.get(id=trip_id, user=self.request.user)
        serializer.save(trip=trip)

class ToDoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ToDoItem.objects.filter(trip__user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_trip_complete(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id, user=request.user)
        trip.status = 'Completed'
        trip.save()
        return Response({
            "message": "Trip marked as completed",
            "trip_id": trip.id,
            "status": trip.status
        }, status=status.HTTP_200_OK)
    except Trip.DoesNotExist:
        return Response({
            "message": "Trip not found"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def photos_view(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id, user=request.user)
    except Trip.DoesNotExist:
        return Response({"message": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        photos = Photo.objects.filter(trip=trip)
        serializer = PhotoSerializer(photos, many=True)
        return Response({"trip_id": trip_id, "photos": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(trip=trip)
            return Response({
                "message": "Photo uploaded successfully",
                "photo": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_photo(request, photo_id):
    try:
        # Get the photo and ensure it belongs to the requesting user
        photo = Photo.objects.get(id=photo_id, trip__user=request.user)
    except Photo.DoesNotExist:
        return Response({"message": "Photo not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Delete the photo
    photo.delete()
    return Response({"message": "Photo deleted successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_moment(request, trip_id):
    try:
        trip = Trip.objects.get(id=trip_id, user=request.user)
    except Trip.DoesNotExist:
        return Response({"message": "Trip not found"}, status=404)

    description = request.data.get('description')
    if not description:
        return Response({"message": "Description is required"}, status=400)

    moment = FavoriteMoment.objects.create(trip=trip, description=description)
    serializer = FavoriteMomentSerializer(moment)
    return Response(serializer.data, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_user_trips(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)
    
    # Only show completed trips
    trips = Trip.objects.filter(user=target_user, status='Completed')
    serializer = TripSerializer(trips, many=True)
    return Response({"trips": serializer.data})