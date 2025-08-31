from rest_framework import serializers
from .models import Trip, ToDoItem, Photo, FavoriteMoment

class ToDoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoItem
        fields = ['id', 'trip', 'task_descri', 'is_complete']
        read_only_fields = ['trip']  # Trip is set via URL, not manually

class FavoriteMomentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMoment
        fields = ['id', 'description']

class TripSerializer(serializers.ModelSerializer):
    todos = ToDoItemSerializer(many=True, read_only=True)
    favorite_moments = FavoriteMomentSerializer(many=True, read_only=False)


    class Meta:
        model = Trip
        fields = [
            'id', 'user', 'title', 'location', 'start_date', 'end_date',
            'trip_type', 'notes', 'review', 'status', 'budget_range', 'todos', 'favorite_moments'
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        favorite_moments_data = validated_data.pop('favorite_moments', [])
        trip = super().create(validated_data)
        for moment_data in favorite_moments_data:
            FavoriteMoment.objects.create(trip=trip, **moment_data)
        return trip

    def update(self, instance, validated_data):
        favorite_moments_data = validated_data.pop('favorite_moments', None)
        instance = super().update(instance, validated_data)

        if favorite_moments_data is not None:
            # Clear old ones
            instance.favorite_moments.all().delete()
            # Recreate
            for moment_data in favorite_moments_data:
                FavoriteMoment.objects.create(trip=instance, **moment_data)

        return instance

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'trip', 'image', 'description']
        read_only_fields = ['trip']