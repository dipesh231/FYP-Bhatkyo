from django.db import models
from multiselectfield import MultiSelectField
from Accounts.models import User, UserProfile

# Create your models here.
class Service(models.Model):
    
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    service_picture = models.ImageField(upload_to='service/servicePicture')
    description = models.TextField()

    def __str__(self):
        return self.name

class Shop(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="userprofile", on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=50)
    shop_image = models.ImageField(upload_to='shop/shop-image', blank=True, null=True)
    shop_lisence = models.ImageField(upload_to='shop/license', blank=True, null=True)
    services = models.ManyToManyField(Service)  # Many-to-Many relationship with Service model
    VERIFICATION_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
    )    
    vehicle_choices = (
        ('two_wheelers', 'Two Wheelers'),
        ('four_wheelers', 'Four Wheelers'),
        ('both', 'Both'),
    )
    vehicles = models.CharField(max_length=100, choices=vehicle_choices)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shop_name

