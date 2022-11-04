from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product

# Create your views here.
def index(request):
    products = Product.objects.all().filter(is_available=True)
    price = request.session['total_price']
    context = {
        'products': products,
        'price':price,
    }
    return render(request, 'home/index.html', context)