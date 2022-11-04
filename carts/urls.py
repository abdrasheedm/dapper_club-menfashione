from django.urls import path
from . import views

urlpatterns = [
      path('',views.cart, name="cart"),
      path('add-to-cart',views.add_to_cart, name="add_to_cart"),
      path('delete-from-cart',views.cart_delete, name="cart_delete"),




]