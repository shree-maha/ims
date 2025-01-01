from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username',)
from django.contrib import admin
from .models import Product, Order

admin.site.register(Product)
admin.site.register(Order)