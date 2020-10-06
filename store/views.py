from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *

# DATA FUNCTIONS

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.total:
        order.complete = True
    order.save()

    if order.delivery:
        DeliveryAddress.objects.create(
            customer=customer,
            order=order,
            address=data['delivery']['address'],
            city=data['delivery']['city'],
            state=data['delivery']['state'],
            zipcode=data['delivery']['zipcode'],
        )


    return JsonResponse('Payment submitted.', safe=False)

def updateOrder(request):
    if(request.user.is_authenticated):
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)

        order.delivery = not order.delivery
        order.save()

        if(order.delivery):
            return JsonResponse('Order changed to delivery', safe=False)
        else:
            return JsonResponse('Order changed to takeout', safe=False)
    else: 
        test = 'x'
    

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity+=1
    elif action == 'remove':
        orderItem.quantity-=1


    orderItem.save()

    if orderItem.quantity <= 0 or action == 'delete':
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

# ALL THE MAIN PAGES
    # STORE
    # CART
    # CHECKOUT 

def store(request, productType = None):
    products = Product.objects.all()
    productTypes = ProductType.objects.all()

    context = {'products':products, 'productTypes': productTypes, 'productType': productType}

    #context.update(getPizzaOptions())
    context.update(cartData(request))

    return render(request, 'store/store.html', context)

def cart(request):
    context = {}
    #context.update(getPizzaOptions())
    context.update(cartData(request))
    


    return render(request, 'store/cart.html', context)

def checkout(request):

    context = {}
    #context.update(getPizzaOptions())
    context.update(cartData(request))
    
    return render(request, 'store/checkout.html', context)

def order_complete(request):
    return render(request, 'store/order_complete.html', {})