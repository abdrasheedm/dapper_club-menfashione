from django.urls import path
from . import views

urlpatterns = [
    path('pay-with-razorpay', views.pay_with_razorpay, name='pay_with_razorpay'),
    path('my-orders', views.my_orders, name='my_orders'),
    

]