from django.urls import path
from . import views

urlpatterns = [
    path('pay-with-razorpay', views.pay_with_razorpay, name='pay_with_razorpay'),
    path('order-complete', views.order_complete, name='order-complete'),
    

]