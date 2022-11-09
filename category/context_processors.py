from .models import Category, Brand, Size, Color
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
    colors = ProductAttribute.objects.distinct().values('color__name', 'color__id', 'color__color_code')
    # sizes = ProductAttribute.objects.distinct().values('size__size', 'size__id')
    prods = Product.objects.all()
    data = {
        'cats':cats,
        'brands':brands,
        'colors':colors,
        # 'sizes':sizes,
        'prods':prods,
    }
    return data