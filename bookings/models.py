from django.db import models
from Accounts.models import User
from mechanic_shop.models import Service, Shop

class BookService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
    services = models.ForeignKey(Service, related_name='booked_services', on_delete=models.CASCADE, null=True)
    vehicle_choices = (
        ('two_wheelers', 'Two Wheelers'),
        ('four_wheelers', 'Four Wheelers'),
        ('both', 'Both'),
    )
    vehicles = models.CharField(max_length=100, choices=vehicle_choices, null=True)
    problem_description = models.TextField()
    STATUS = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    location = models.CharField(max_length=150, null = True)
    time = models.TimeField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.problem_description

class RateBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_service = models.ForeignKey(BookService, on_delete=models.CASCADE, null=True)
    review = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.user.name