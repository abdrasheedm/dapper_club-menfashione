from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from orders.models import Payment, Order, OrderProduct
from carts.models import CartItem
from store.models import ProductAttribute


# authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(
#     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def order_payment(request):
    payment = Payment()
    payment.user = request.user
    if request.POST.get('payment_id'):
        payment.payment_id = request.POST.get('payment_id') 
    payment.payment_method = request.POST.get('payment_mode')
    payment.amount_paid = request.POST.get('amount_paid') 
    payment.status=True
    payment.save()

    print(payment)

    order_number = request.POST.get('order_number')
    order = Order.objects.get(user=request.user, order_number=order_number)
    order.payment = payment
    order.is_ordered = True
    order.status ='Pending' 
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:
        OrderProduct.objects.create(
            order=order,
            payment=payment,
            user=request.user,
            product=cart_item.product,
            quantity=cart_item.quantity,
            product_price=cart_item.product.product.price,
            ordered = True
        )
        product = ProductAttribute.objects.get(id=cart_item.product.id)
        product.stock -= cart_item.quantity
        product.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete() 
    return JsonResponse({'status':"Your order has been placed successfully "})
 


def order_complete(request):
    order_number = request.GET.get('order_number')
    order = Order.objects.get(user=request.user, order_number=order_number)
    ordered_products = OrderProduct.objects.filter(order=order)
    total_amount = 0
    for item in ordered_products:
        total_amount += (item.product_price * item.quantity)
    tax = round((18 * float(total_amount))/100)
    sub_total = total_amount - tax
    context = {
        'order':order,
        'ordered_products':ordered_products,
        'sub_total':sub_total,
        'tax':tax,
        'total_amount':total_amount,
    }
    return render(request, 'orders/payment_complete.html', context)