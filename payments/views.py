from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse

from orders.models import Payment, Order, OrderProduct
from carts.models import CartItem


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def pay_with_razorpay(request):
    payment = Payment()
    payment.user = request.user
    payment.payment_id = request.POST.get('payment_id')
    payment.payment_method = request.POST.get('payment_mode')
    payment.amount_paid = request.POST.get('amount_paid')
    payment.status=True
    payment.save()

    print(payment)

    order_number = request.POST.get('order_number')
    order = Order.objects.get(user=request.user, order_number=order_number)
    order.payment = payment
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
    # order_product.product = 
    # order_product.quantity = 

    return HttpResponse("hai")