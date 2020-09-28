from django.shortcuts import render
from .models import Customer, Product, Order, OrderItem, ShippingAddress
#para devolver objetos json
from django.http import JsonResponse
#para obtener json
import json

import datetime

def store(request):
    if request.user.is_authenticated:
        #obtener usuario autenticado
        customer = request.user.customer
        #consultar o crear el objeto
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        #obtener los elementos de esa orden
        items = order.orderitem_set.all()
        #obtener la cantidad de items
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total':0,
            'get_cart_items':0,
            'shipping':False
        }
        cartItems = order['get_cart_items']

    #obtener todos los productos
    products = Product.objects.all()
    context = {
        'products':products,
        'cartItems':cartItems
    }
    return render(request, 'store.html', context)

def cart(request):

    if request.user.is_authenticated:
        #obtener usuario autenticado
        customer = request.user.customer
        #consultar o crear el objeto
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        #obtener los elementos de esa orden
        items = order.orderitem_set.all()
        #obtener la cantidad de items
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total':0,
            'get_cart_items':0,
            'shipping':False
        }

    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        #obtener usuario autenticado
        customer = request.user.customer
        #consultar o crear el objeto
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        #obtener los elementos de esa orden
        items = order.orderitem_set.all()
        #obtener la cantidad de items
        cartItems = order.get_cart_items
    else:
        items = []
        order = {
            'get_cart_total':0,
            'get_cart_items':0,
            'shipping':False
        }

    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'checkout.html', context)

def updateItem(request):
    #cargar los datos del json en el backend
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    #mostrando los datos en el backend
    print('Action:', action, 'productId:', productId)

    #obtener el usuario y el id del producto
    customer = request.user.customer
    product = Product.objects.get(id = productId)

    #crear u obtener la orden
    order, created = Order.objects.get_or_create(customer = customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    #Cambiar la cantidad de productos
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

#Manejo de la compra
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    print('Data:', request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )

            #print('Datos:', customer, order, address, city, state, zipcode)

    else:
        print('User is not logged in...')

    return JsonResponse('Payment complete!', safe = False)

