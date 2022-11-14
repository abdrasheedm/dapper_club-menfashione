from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('search', views.search, name='search'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('brand/<slug:brand_slug>/', views.store_by_brand, name='product_by_brand'),
    path('color/<slug:color_slug>/', views.product_by_color, name='product_by_color'),
    path('size/<slug:size_slug>/', views.product_by_size, name='product_by_size'),
    path('price/<slug:price_id>/', views.products_by_price, name='products_by_price'),

    path('<slug:sub_category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),

]