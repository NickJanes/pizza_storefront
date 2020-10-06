import json
from .models import *

#def getPizzaOptions():
    #toppings = Topping.objects.all()
    #sizes = PizzaSize.objects.all()

    #return {'size': sizes, 'topping': toppings}

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {'delivery':0}

    items = []
    order = {'total':0, 'quantity':0, 'delivery':0}

    try:
        order['delivery'] = cart['delivery']
        for i in cart:
            order['quantity'] += cart[i]['quantity']
            
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']
            
            order['total'] += total
            item = {
                'product': product,
                'quantity': cart[i]['quantity'],
                'total': total
            }
            items.append(item)
    except:
        pass

    return {'items':items, 'order':order}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.order_item.all()
    else:
        cookieData = cookieCart(request)
        order = cookieData['order']
        items = cookieData['items']
    
    return {'items':items, 'order':order}

def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )
    order.delivery = cookieData['order']['delivery']
    
    for item in items:
        product = item['product']
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )
    return customer, order