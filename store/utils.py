import json
from .models import Customer, Product, Order, OrderItem, ShippingAddress

def cookieCart(request):
    try:
        #Covertir el json en formato legible para python
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

    items = []
    order = {
        'get_cart_total':0,
        'get_cart_items':0,
        'shipping':False
    }
    
    cartItems = order['get_cart_items']

    #Recorrer el objeto cart
    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            #Total de items y total price
            product = Product.objects.get(id = i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            #Elementos del carrito
            item  = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}


def cartData(request):
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
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return{'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):

    print('User is not logged in...')
    print('COOKIE:', request.COOKIES)

    #Registro de cliente anonimo en la DB
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.save()

    #Registro de la orden anonimo

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    #Recorrer objeto items para corroborar que el producto selecciona corresponde al catalogo
    for item in items:
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    
    return customer, order