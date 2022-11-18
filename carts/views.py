from django.shortcuts import render,redirect, get_object_or_404
from django.http.response import JsonResponse
from store.models import Product, ProductAttribute
from .models import Cart, CartItem,WishlistItem
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required



# Create your views here.




#Add To Cart

def add_to_cart(request):
    # del request.session['cartdata']   
    current_user=request.user
    # cart_prod={}
    # cart_prod[str(request.GET['id'])]={
    #     'name':request.GET['name'],
    #     'image':request.GET['image'],
    #     'qty':request.GET['qty'],
    #     'color':request.GET['color'],
    #     'size':request.GET['size'],
    #     'price':request.GET['price'],
    # }

    product = ProductAttribute.objects.get(id__exact=request.GET['id'])
    try:
        cart = Cart.objects.get(cart_id = request.session.session_key) # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = request.session.session_key)
        cart.save()
    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            cart_item.quantity = request.GET['qty']
            cart_item.save()
            messages.success(request, 'Item added to cart.')
            

            
        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = request.GET['qty'],
                    user = current_user,
                )
            messages.success(request, 'Item added to cart.')
            
    else:
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            cart_item.quantity = request.GET['qty']
            cart_item.save()
            messages.success(request, 'Item added to cart.')

                # existing_variations -> database
                # current variation -> product_variation
                # item_id -> database
        else:
            cart_item = CartItem.objects.create(
                    product = product,
                    quantity = request.GET['qty'],
                    cart = cart,
                )
            messages.success(request, 'Item added to cart.')
            
    # return redirect('cart')
    # if 'cartdata' in request.session:
    #         cart = Cart.objects.get(cart_id = request.session.session_key)
    #         if str(request.GET['id']) in request.session['cartdata']:
    #             cart_data=request.session['cartdata']
    #             cart_data[str(request.GET['id'])]['qty']=int(cart_prod[str(request.GET['id'])]['qty'])
    #             cart_data.update(cart_data)
    #             request.session['cartdata']=cart_data
    #             print("if done")
    #         else:

    #             cart_data=request.session['cartdata']
    #             print(cart_data)
    #             cart_data.update(cart_prod)
    #             request.session['cartdata']=cart_data
    #             CartItem.objects.create(user=request.user, product=ProductAttribute.objects.get(id=request.GET['id']), cart=cart, quantity= request.GET['qty'])
    #             print("else done")


    # else:
    #     request.session['cartdata']=cart_prod
    #     print("hai")
    #     # cart = request.session.session_key
    #     # print(cart)
    #     print(request.session.session_key)

    #     cart = Cart.objects.create(
    #         cart_id=request.session.session_key
    #     )
    
    #     print(request.session.session_key)
    #     if request.user.is_authenticated:
    #         CartItem.objects.create(user=request.user ,product=ProductAttribute.objects.get(id=request.GET['id']), cart=cart, quantity= request.GET['qty'])

    #     else:
    #         CartItem.objects.create(product=ProductAttribute.objects.get(id=request.GET['id']), cart=cart, quantity= request.GET['qty'])



        # cart_item = CartItem()
        # cart_item.user = request.user
        # cart_item.product = ProductAttribute.objects.get(id=request.GET['id'])
        # cart_item.cart = cart
        # cart_item.quantity = request.GET['qty']
        # print("done")
    return JsonResponse({'single_product':'success'})


def cart(request):
    print("ha ca")
    current_user=request.user
    context = {}
    try:
        # print("ha3")

        if current_user.is_authenticated:
            cart_items = CartItem.objects.filter(user=current_user, is_active=True)
            print("ha1")

        else:
            print("ha2")
            cart = Cart.objects.get(cart_id=request.session.session_key)
            print("ha5")

            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            print("ha4")

        total_amount = 0
        for cart_item in cart_items:
        # for p_id,item in request.session['cartdata'].items():

            # total_amount += int(item['qty'])*float(item['price'])
            total_amount += (cart_item.product.product.price * cart_item.quantity)


        tax = round((18 * float(total_amount))/100)
        sub_total = total_amount - tax
        context = {
            'total_amount':total_amount,
            'tax':tax,
            'sub_total':sub_total,
            'cart_items':cart_items,
            # 'single_product':request.session['cartdata']
        }
        print("ha cart0000000000")
    except:
        print("hao")
        pass #just ignore
    # if 'cartdata' in request.session:
    #     print('hai')
    #     cart = Cart.objects.get(cart_id=request.session.session_key)
    #     cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    #     total_amount = 0
    #     for cart_item in cart_items:
    #     # for p_id,item in request.session['cartdata'].items():

    #         # total_amount += int(item['qty'])*float(item['price'])
    #         total_amount += (cart_item.product.product.price * cart_item.quantity)


    #     tax = round((18 * float(total_amount))/100)
    #     sub_total = total_amount - tax
    #     context = {
    #         'total_amount':total_amount,
    #         'tax':tax,
    #         'sub_total':sub_total,
    #         'cart_items':cart_items,
    #         # 'single_product':request.session['cartdata']
    #     }
    #     # request.session['total_price'] = total_amount
    #     print(total_amount)
    print("ha cart1111111111111111111")
    return render(request, 'store/cart.html', context)

# delete cart item

def cart_delete(request, prod_id):
    # p_id = str(request.GET['id'])
    current_user=request.user 
    product = get_object_or_404(ProductAttribute, id=prod_id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.get(user=current_user, product=product)
    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    print("ha cart")
    return redirect('cart')

# update cart item 

def cart_update(request):
    current_user=request.user
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    product = get_object_or_404(ProductAttribute, id=p_id)
    if current_user.is_authenticated:
        cart_item=CartItem.objects.get(user=current_user, product=product)
    else:
        cart = Cart.objects.get(cart_id=request.session.session_key)
        cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity = p_qty
    cart_item.save()


    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, is_active=True)
        print("ha1")

    else:
        print("ha2")
        cart = Cart.objects.get(cart_id=request.session.session_key)
        print("ha5")

        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        print("ha4")

    total_amount = 0
    for cart_item in cart_items:

        total_amount += (cart_item.product.product.price * cart_item.quantity)


        tax = round((18 * float(total_amount))/100)
        sub_total = total_amount - tax
        context = {
            'total_amount':total_amount,
            'tax':tax,
            'sub_total':sub_total,
            'cart_items':cart_items,
            # 'single_product':request.session['cartdata']
        }

    # return redirect('cart')

    # if 'cartdata' in request.session:
    #     if p_id in request.session['cartdata']:
    #         cart_data = request.session['cartdata']
    #         cart_data[str(request.GET['id'])]['qty'] = p_qty
    #         request.session['cartdata']=cart_data

    # total_amount = 0
    # for p_id, item in request.session['cartdata'].items():
    #     total_amount += int(item['qty'])*float(item['price'])
    # tax = (18 * float(total_amount))/100
    # sub_total = total_amount - tax
    # context = {
    #     'total_amount':total_amount,
    #     'tax':tax,
    #     'sub_total':sub_total,
    #     'single_product':request.session['cartdata']
    # }
    t = render_to_string('store/ajax/cart-list.html', context)
    return JsonResponse({'data':t})

@login_required(login_url='signin')
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print(user, product)
    is_wished = WishlistItem.objects.filter(product=product)
    if not is_wished:
        print("yes")
        product = WishlistItem.objects.create(
            user=user,
            product=product,
            is_active=True,
        )
        messages.success(request, 'Item added to wishlist.')
    
    else:
        print("no")

        messages.success(request, 'Item already in wishlist.')
    
    return JsonResponse({'single_product':'success'})


@login_required(login_url='signin')
def wishlist(request):
    products = WishlistItem.objects.filter(user=request.user, is_active=True)

    return render(request, 'store/wishlist.html', {'products':products})


def delete_from_wishlist(request):
    prod_id = request.GET['id']
    print(prod_id)
    product = Product.objects.get(id=prod_id)
    wishlist_item = WishlistItem.objects.get(product=product)
    wishlist_item.delete()
    return redirect('wishlist')
