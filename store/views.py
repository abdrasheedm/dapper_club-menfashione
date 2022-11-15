
from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductAttribute
from category.models import Category, Brand, Color, Size, PriceFilter
from carts.models import Cart, CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def store(request, category_slug=None) :
    # if not request.session.session_key:
    #     print('hai')
    #     request.session.create()
    categories = None
    products = None
    print(category_slug)

    # brands = Brand.objects.all()

    if category_slug != None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(sub_category__category=categories)
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    # elif brand_slug != None:
    #     print("hai")
    #     brands = get_object_or_404(Brand, slug=brand_slug)
    #     print("helllo")

    #     products = ProductAttribute.objects.filter(product__brand = brands)
    #     print("pooi")
    #     products_count = products.count()


    else:
        print("else")

        # products = ProductAttribute.objects.distinct().values('product__product_name', 'price', 'product__image1')
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
        # single_product = Product.objects.get(sub_category__slug=sub_category_slug, slug=product_slug)
        # product_attr = ProductAttribute.objects.get(product__slug=product_slug)
        product = Product.objects.get(slug=product_slug)
        related_products = Product.objects.filter(sub_category__category=product.sub_category.category).exclude(slug=product_slug)[:4]
        colors=ProductAttribute.objects.filter(product=product).values('color__id','color__name','color__color_code').distinct()
        sizes=ProductAttribute.objects.filter(product=product).values('id','size__id','size__size','color__id').distinct()
        price = ProductAttribute.objects.filter(product=product).first()
        print(sizes.count())
        print(product.price)
        

    except Exception as e:
        raise e

    context = {
        # 'single_product':single_product,
        # 'product_attr' : product_attr,
        'related':related_products,
        'product':product,
        'sizes':sizes,
        'colors':colors,
        'price':price,

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
        # 'single_product':request.session['cartdata']
    }
    return render(request, 'store/checkout.html', context)





