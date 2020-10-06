from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)
admin.site.register(ProductOption)
admin.site.register(ProductType)
admin.site.register(OptionType)
#admin.site.register(PizzaSize)
#admin.site.register(Topping)