from django.contrib.auth.models import User
from django.db import models

class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    seats_available = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.from_location} → {self.to_location} ({self.departure_time})"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('accepted', 'Подтверждено'),
        ('rejected', 'Отклонено'),
    )
    
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    seats_requested = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)