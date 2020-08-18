
/* Add click input to takeout/delivery button
*/
var takeoutButton = $('.takeout-btn')
for(i = 0; i < takeoutButton.length; i++) {
    takeoutButton[i].addEventListener('click', function(){
        if(user == 'AnonymousUser') {
            UpdateTakeoutOrDeliveryCookie()
        } else {
            UpdateTakeoutOrDelivery()
        }
        
    })
}


/*  Add click input to 'add to cart' buttons on store page
    click function -
    logged in user - updates cart in DB
    Guest user - updates cart cookie
*/
var updateButtons = $('.update-cart')
for(i = 0; i < updateButtons.length; i++) {
    updateButtons[i].addEventListener('click', function(){
        var productID = this.dataset.product
        var action = this.dataset.action

        if(user == 'AnonymousUser') {
            addCookieItem(productID, action)
        } else {
            UpdateUserOrder(productID, action)
        }
    })
}

//Changes to pickup/delivery in DB
function UpdateTakeoutOrDelivery() {
    var url = '/update_order/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}

function UpdateTakeoutOrDeliveryCookie() {
    if(cart['delivery']) {
        cart['delivery'] = false
    } else {
        cart['delivery'] = true
    }

    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}

//For operations on cart items
function UpdateUserOrder(productID, action) {
    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productID': productID, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}


//Performs operations on guest user cart managed by cookies
function addCookieItem(productID, action) {
    if(action == 'add') {
        if(cart[productID] == undefined){
            cart[productID] = {'quantity':1}
        } else {
            cart[productID]['quantity'] += 1
        }
    }

    if(action == 'remove') {
        cart[productID]['quantity'] -= 1
        
        if (cart[productID]['quantity'] <= 0) {
            delete cart[productID]
        }
    }

    if(action == 'delete') {
        delete cart[productID]
    }
    console.log(cart['quantity'])

    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}