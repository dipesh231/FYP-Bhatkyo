from django.db import models

from Accounts.models import User
from mechanic_shop.models import Shop

class Product(models.Model):
    user = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null = True, blank = True)
    description = models.TextField(max_length=250, blank=True)
    total_quantity = models.IntegerField()
    availability  = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to='products/product_image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
class ProductPayment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    