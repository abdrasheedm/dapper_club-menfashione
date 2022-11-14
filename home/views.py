from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductAttribute
from category.models import Category, Brand
from .models import Banner


# Create your views here.
def index(request):
    banners = Banner.objects.all().order_by('-id')
    if not request.session.session_key:
        print('hai')
        request.session.create()
    # products = ProductAttribute.objects.filter(product__is_featured=True).values('product__product_name','price','product__image1').distinct().order_by('-id')
    products = Product.objects.filter(is_featured=True).order_by('-id')
    context = {
        'products':products,
        'banners':banners,
    }
    
    return render(request, 'home/index.html', context)


