
from django.shortcuts import get_object_or_404, render
from store.models import Product, ProductAttribute
from category.models import Category, Brand

# Create your views here.
def store(request, category_slug=None) : 
    
    print("looooi")

    categories = None
    products = None
    brands = None
    print(category_slug)

    # brands = Brand.objects.all()

    if category_slug != None:
        print("cat")    

        categories = get_object_or_404(Category, slug=category_slug)
        products = ProductAttribute.objects.filter(product__sub_category__category=categories)
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
        products_count = products.count()


    context = {
        'products': products,
        'products_count':products_count,
        # 'brands':brands,

    }
    return render(request, 'store/shop.html', context)


def product_detail(request, sub_category_slug, product_slug):
    try:
        # single_product = Product.objects.get(sub_category__slug=sub_category_slug, slug=product_slug)
        # product_attr = ProductAttribute.objects.get(product__slug=product_slug)
        product = Product.objects.get(slug=product_slug)
        related_products = Product.objects.filter(sub_category__category=product.sub_category.category).exclude(slug=product_slug)[:4]
        colors=ProductAttribute.objects.filter(product=product).values('color__id','color__name','color__color_code').distinct()
        sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__size','price','color__id').distinct()
        print(sizes.count())
        

    except Exception as e:
        raise e

    context = {
        # 'single_product':single_product,
        # 'product_attr' : product_attr,
        'related':related_products,
        'product':product,
        'sizes':sizes,
        'colors':colors,

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

        products = ProductAttribute.objects.filter(product__brand = brands)
        print("pooi")
        products_count = products.count()


    else:
        print("else")

        products = ProductAttribute.objects.all()
        products_count = products.count()


    context = {
        'products': products,
        'products_count':products_count,

    }
    return render(request, 'store/shop.html', context)


def search(request):
    q = request.GET['q']
    products = ProductAttribute.objects.filter(product__product_name__icontains=q).order_by('-id')
    products_count = products.count()
    context = {
        'products': products,
        'products_count':products_count,
        # 'brands':brands,

    }
    return render(request, 'store/search.html', context)






