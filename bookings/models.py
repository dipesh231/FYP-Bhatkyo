from django.db import models
from Accounts.models import User
from products.models import Product
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
    location = models.CharField( null = True)
    latitude = models.CharField(max_length = 20, blank = True, null = True)
    longitude = models.CharField(max_length = 20, blank = True, null = True)

    date =   models.DateTimeField();
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.problem_description
    
def get_vehicles_display(self):
        return dict(self.vehicle_choices).get(self.vehicles, '')

class RateBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book_service = models.ForeignKey(BookService, on_delete=models.CASCADE, null=True)
    review = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return self.user.name
# models.py
class Invoice(models.Model):
    booking = models.OneToOneField(BookService, on_delete=models.CASCADE, related_name='invoice')
    service_hours = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)