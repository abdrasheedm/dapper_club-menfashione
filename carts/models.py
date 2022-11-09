from django.db import models
from accounts.models import Account
from store.models import Product

# Create your models here.

    

class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    

