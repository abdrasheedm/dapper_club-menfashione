from .models import Category, Brand, Size, Color, PriceFilter
from carts.models import CartItem
from store.models import Product, ProductAttribute

# def menu_links(request):
#     links = Category.objects.all()
#     return dict(links = links)

# def brand_links(request):
#     links = Brand.objects.all()
#     return dict(brand_links = links)

def get_filters(request):
    # cats = Product.objects.distinct().values('sub_category__category__category_name', 'sub_category__category__id')
    cats = Category.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    sizes = Size.objects.all()
    prices = PriceFilter.objects.all()
    # colors = ProductAttribute.objects.distinct().values('color__name', 'color__id', 'color__color_code')
    # sizes = ProductAttribute.objects.distinct().values('size__size', 'size__id')
    prods = Product.objects.all()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart=request.session.session_key)

    data = {
        'cats':cats,
        'brands':brands,
        'colors':colors,
        'sizes':sizes,
        'prods':prods,
        'prices':prices,
        'cart_items':cart_items,
    }
    return data