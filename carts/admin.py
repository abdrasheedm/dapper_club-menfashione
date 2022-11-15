from django.contrib import admin
from .models import  Cart, CartItem

# Register your models here.

admin.site.register(Cart)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product','user', 'quantity','is_active')
    list_editable = ('is_active',)
admin.site.register(CartItem, CartItemAdmin)



