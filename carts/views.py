from django.shortcuts import render,redirect
from django.http.response import JsonResponse
from store.models import Product, ProductAttribute
from .models import Cart
from django.template.loader import render_to_string


# Create your views here.




#Add To Cart

def add_to_cart(request):
    # del request.session['cartdata']   
    cart_prod={}
    cart_prod[str(request.GET['id'])]={
        'name':request.GET['name'],
        'image':request.GET['image'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }

    product = Product.objects.get(id__exact=request.GET['id'])
    if 'cartdata' in request.session:
            if str(request.GET['id']) in request.session['cartdata']:
                cart_data=request.session['cartdata']
                cart_data[str(request.GET['id'])]['qty']=int(cart_prod[str(request.GET['id'])]['qty'])
                cart_data.update(cart_data)
                request.session['cartdata']=cart_data
            else:
                cart_data=request.session['cartdata']
                print(cart_data)
                cart_data.update(cart_prod)
                request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_prod
    return JsonResponse({'single_product':request.session['cartdata']})


def cart(request):
    context = {}
    if 'cartdata' in request.session:
        total_amount = 0
        for p_id,item in request.session['cartdata'].items():

            total_amount += int(item['qty'])*float(item['price'])

        tax = round((18 * float(total_amount))/100)
        sub_total = total_amount - tax
        context = {
            'total_amount':total_amount,
            'tax':tax,
            'sub_total':sub_total,
            'single_product':request.session['cartdata']
        }
        # request.session['total_price'] = total_amount
    return render(request, 'store/cart.html', context)

# delete cart item

def cart_delete(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data

    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty'])*float(item['price'])
    tax = (18 * float(total_amount))/100
    sub_total = total_amount - tax
    context = {
        'total_amount':total_amount,
        'tax':tax,
        'sub_total':sub_total,
        'single_product':request.session['cartdata']
    }
    t = render_to_string('store/ajax/cart-list.html', context)
    return JsonResponse({'data':t})

# update cart item 

def cart_update(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata']=cart_data

    total_amount = 0
    for p_id, item in request.session['cartdata'].items():
        total_amount += int(item['qty'])*float(item['price'])
    tax = (18 * float(total_amount))/100
    sub_total = total_amount - tax
    context = {
        'total_amount':total_amount,
        'tax':tax,
        'sub_total':sub_total,
        'single_product':request.session['cartdata']
    }
    t = render_to_string('store/ajax/cart-list.html', context)
    return JsonResponse({'data':t})
