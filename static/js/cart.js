//Capturar el boton en la variable updateBtns
var updateBtns = document.getElementsByClassName('update-cart')

//CICLO para acumular cada click que se de sobre cada boton de Add to Cart
for(i=0; i < updateBtns.length; i++){
    //Cada vez que se le click al boton
    updateBtns[i].addEventListener('click', function(){
        //guardar id
        var productId = this.dataset.product
        //guardar accion
        var action = this.dataset.action

        console.log('productId:', productId, 'Action:', action)
        console.log('User:', user)

        if(user === 'AnonymousUser'){
            //console.log('Not looged in')
            addCookieItem(productId, action)
        }else{
            //console.log('User is logged sending data...')
            updateUserOrder(productId, action)
        }
    })
}

//MANEJO DEL USUARIO ANONIMO
function addCookieItem(productId, action){
    console.log('Not logget in...')

    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {
                'quantity':1
            }
        }else{
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0 ){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('Cart', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + "; domain = ; path = /"
    location.reload()
}


function updateUserOrder(productId, action){
    console.log('User is logged in, sending data...')

    //Mandar los datos al backend
    var url = '/update_item'

    // a traves de fetch
    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        //Datos que se enviaran al backend
        body:JSON.stringify({'productId': productId, 'action': action})
    })


    .then((response) => {
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}
