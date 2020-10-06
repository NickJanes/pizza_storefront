from django.db import models
from django.contrib.auth.models import User

# Create your models here.
"""
class Topping(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

class PizzaSize(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)
"""

class ProductType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

class OptionType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)

class ProductOption(models.Model):
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True)
    optionType = models.ForeignKey(OptionType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(null=True, blank=True)
    productType = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name + ": $" + str(self.price)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)
    delivery = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer) + " ordered on " + str(self.date_order) + " with a transaction ID of : " + str(self.transaction_id)

    def total(self):
        order_items = self.order_item.all()
        tot = sum([item.total for item in order_items])
        return tot

    def quantity(self):
        order_items = self.order_item.all()
        tot = sum([item.quantity for item in order_items])
        return tot

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True, blank=True, related_name="order_item")
    quantity = models.IntegerField(default = 0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.quantity) + " orders of " + str(self.product.name)

    @property
    def total(self):
        return self.quantity * self.product.price

class DeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)  
    city = models.CharField(max_length=200, null=True)  
    state = models.CharField(max_length=200, null=True)  
    zipcode = models.CharField(max_length=200, null=True)  
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)
