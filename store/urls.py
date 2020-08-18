from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order_complete/", views.order_complete, name="order_complete"),
    path("update_item/", views.updateItem, name="update_item"),
    path("update_order/", views.updateOrder, name="update_order"),
    path("process_order/", views.processOrder, name="process_order")
]
