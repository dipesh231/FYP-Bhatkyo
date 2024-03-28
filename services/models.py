from django.db import models



# Create your models here.

# class ServiceItem(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     vehicles = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     services = models.ForeignKey(Shop, on_delete=models.CASCADE)
#     food_title = models.CharField(max_length=50)
#     slug = models.SlugField(max_length=100, unique=True)
#     description = models.TextField(max_length=250, blank=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='foodimages')
#     is_available = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.food_title