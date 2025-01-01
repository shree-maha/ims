from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
from django.db import models

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Added image field

    def __str__(self):
        return self.name

def update_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False  # Return False if not enough stock
class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Placed")  # Order status (e.g., 'Placed', 'Shipped', 'Delivered')
    @property
    def total_price(self):
        return self.product.price * self.quantity  
    def __str__(self):
        return f"Order by {self.customer.username} - {self.product.name} - {self.status}"

