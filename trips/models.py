from django.db import models
from django.contrib.auth.models import User

TRIP_TYPE_CHOICES = [
    ('Solo', 'Solo'),
    ('Business', 'Business'),
    ('Family', 'Family'),
    ('Couple', 'Couple'),
]

BUDGET_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

TRIP_STATUS_CHOICES = [
    ('Future', 'Future'),
    ('Completed', 'Completed'),
]

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPE_CHOICES)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='Future')
    budget_range = models.CharField(max_length=20, choices=BUDGET_CHOICES, blank=True, null=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class ToDoItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='todos')
    task_descri = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task_descri} ({'Done' if self.is_complete else 'Pending'})"


class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='trip_photos/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Photo for {self.trip.title}"

class FavoriteMoment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='favorite_moments')
    description = models.TextField()

    def __str__(self):
        return f"Favorite moment for {self.trip.title}"