
from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductAttribute
from accounts.models import UserProfile
from category.models import Category, Brand, Color, Size, PriceFilter
from carts.models import Cart, CartItem, WishlistItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def store(request, category_slug=None) :
    categories = None
    products = None
    print(category_slug)
    in_wishlist = WishlistItem

    if category_slug != None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(sub_category__category=categories) 
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()


    else:
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()


    context = {
        'products': paged_products,
        'products_count':products_count,
        # 'brands':brands,

    }
    return render(request, 'store/shop.html', context)


def product_detail(request, sub_category_slug, product_slug):

    if not request.session.session_key:
        print('hai')
        request.session.create()
    try:
        product = Product.objects.get(slug=product_slug)
        related_products = Product.objects.filter(sub_category__category=product.sub_category.category).exclude(slug=product_slug)[:4]
        colors=ProductAttribute.objects.filter(product=product).values('color__id','color__name','color__color_code').distinct()
        sizes=ProductAttribute.objects.filter(product=product).values('id','size__id','size__size','color__id', 'stock').distinct()
        price = ProductAttribute.objects.filter(product=product).first()
        in_wishlist=WishlistItem.objects.filter(product=product)
        

    except Exception as e:
        raise e

    context = {
   
        'related':related_products,
        'product':product,
        'sizes':sizes,
        'colors':colors,
        'price':price,
        'in_wishlist':in_wishlist,

    }
    return render(request, 'store/product_detail.html', context)


def store_by_brand(request, brand_slug=None):
    
    print("brand")
    products = None
    brands = None

    if brand_slug != None:
        print("hai")
        brands = get_object_or_404(Brand, slug=brand_slug)
        print("helllo")

        products = Product.objects.filter(brand = brands).order_by('-id')
        print("pooi")
        products_count = products.count()


    else:
        print("else")

        products = Product.objects.all()
        products_count = products.count()


    context = {
        'products': products,
        'products_count':products_count,

    }
    return render(request, 'store/shop.html', context)


def search(request):
    q = request.GET['q']
    products = Product.objects.filter(product_name__icontains=q).order_by('-id')
    products_count = products.count()
    context = {
        'products': products,
        'products_count':products_count,
        # 'brands':brands,

    }
    return render(request, 'store/search.html', context)


def product_by_color(request, color_slug):
    colors = get_object_or_404(Color, slug=color_slug)
    print("color")

    products = ProductAttribute.objects.filter(color = colors).order_by('-id')
    print("pooi")
    products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/product_by_color.html', context)


def product_by_size(request, size_slug):
    sizes = get_object_or_404(Size, slug=size_slug)
    print("color")
    print(sizes.count())

    products = ProductAttribute.objects.filter(size = sizes).order_by('-id')
    print("pooi")
    products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/product_by_size.html', context)


def products_by_price(request, price_id):
    price_filter = get_object_or_404(PriceFilter, id=price_id)
    products = Product.objects.filter(price_filter=price_filter).order_by('-id')

    products_count = products.count()
    context = {
        'products':products,
        'products_count':products_count,
    }
    return render(request, 'store/product_by_price.html', context)



@login_required(login_url='signin')
def checkout(request):
    context = {}
    user=request.user
    cart_items=CartItem.objects.filter(user=user, is_active=True)
    userprofile = UserProfile.objects.filter(user=request.user).first()
    print(userprofile.address_line_1)
    
    total_amount = 0
    for cart_item in cart_items:

        total_amount += (cart_item.product.product.price * cart_item.quantity)


    tax = round((18 * float(total_amount))/100)
    sub_total = total_amount - tax
    context = {
        'total_amount':total_amount,
        'tax':tax,
        'sub_total':sub_total,
        'cart_items':cart_items,
        'userprofile':userprofile
        # 'single_product':request.session['cartdata']
    }
    return render(request, 'store/checkout.html', context)





