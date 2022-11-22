from django.shortcuts import render,redirect
from accounts.models import Account
from store.models import Product, ProductAttribute
from orders.models import Order
from category.models import Category
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages





# Create your views here.

@never_cache
@login_required(login_url='signin') 
def manager_dashboard(request):
    if request.user.is_superadmin:

        user_count = Account.objects.filter(is_superadmin=False).count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.filter(is_ordered=True).count()
        category_count = Category.objects.all().count()
        variation_count = ProductAttribute.objects.all().count()
        admin_order_count = Order.objects.filter(user__is_superadmin=True).count()
        

        context = {
            'user_count': user_count,
            'product_count': product_count,
            'order_count' : order_count,
            'category_count' : category_count,
            'variation_count' : variation_count,
            'admin_order_count' : admin_order_count
        }

        return render(request,'manager/manager_dashboard.html',context)
    else:
        return redirect('index')


# Manage users
@never_cache
@login_required(login_url='signin')
def user_management(request):
    if request.method == "POST":
      key = request.POST['key']
      users = Account.objects.filter(Q(first_name__startswith=key) | Q(last_name__startswith=key) | Q(username__startswith=key) | Q(email__startswith=key)).order_by('id')
    else:
        users = Account.objects.filter(is_superadmin=False).order_by('id')

    paginator = Paginator(users,10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users' : paged_users
    }
    return render(request, 'manager/user_management.html',context)


def user_block(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active = False
  user.save()
  return redirect('user_management')

def user_unblock(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active= True
  user.save()
  return redirect('user_management')


def category_management(request):
    categories = Category.objects.all().order_by('id')

    context = {
        'categories' :categories
    }

    return render(request, 'manager/category_management.html',context)


#Mange product
@never_cache
@login_required(login_url='signin')
def product_management(request):
  if request.method == "POST":
    key = request.POST['key']
    products = Product.objects.filter(Q(product_name__icontains=key) | Q(slug__startswith=key) | Q(sub_category__category__category_name__startswith=key)).order_by('id')
  else:
    products = Product.objects.all().order_by('id')

  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)
  
  context = {
    'products': paged_products
  }
  return render(request, 'manager/product_management.html', context)


# Add Product
@never_cache
@login_required(login_url='login')
def add_product(request):
  if request.method == 'POST':
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('product_management')
  else:
    form = ProductForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_product.html', context)


  # Manage Order
@never_cache
@login_required(login_url='signin')
def order_management(request):
  if request.method =="POST":
    key = request.POST['key']
    orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__icontains=key) | Q(user__email__icontains=key) | Q(first_name__startswith=key)).order_by('id')
  else:
    orders = Order.objects.filter(is_ordered=True).order_by('id')
    

  context = {
    'orders': orders
  }
  return render(request, 'manager/order_management.html', context)


  # Manage Variation
@never_cache
@login_required(login_url='signin')
def variation_management(request):
  if request.method == 'POST':
    keyword = request.POST['keyword']
    variations = ProductAttribute.objects.filter(Q(product__product_name__icontains=keyword) | Q(product__sub_category__category__category_name__startswith=keyword) | Q(color__color_name__startswith=keyword | Q(size__size__startswith=keyword)).order_by('id'))
  
  else:
    variations = ProductAttribute.objects.all().order_by('id')
  
  paginator = Paginator(variations, 10)
  page = request.GET.get('page')
  paged_variations = paginator.get_page(page)
  
  context = {
    'variations': paged_variations
  }
  return render(request, 'manager/variation_management.html', context)



# Admin orders
@login_required(login_url='signin')
def admin_order(request):
  current_user = request.user
  if request.method == 'POST':
    keyword = request.POST['keyword']
    orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__contains=keyword) | Q(user__emai__icontains=keyword) | Q(first_name__startswith=keyword) | Q(last_name__startswith=keyword) | Q(phone__startswith=keyword)).order_by('-created_at')
    
  else:
    orders = Order.objects.filter(user=current_user, is_ordered=True).order_by('-created_at')
  
  paginator = Paginator(orders, 10)
  page = request.GET.get('page')
  paged_orders = paginator.get_page(page)
  context = {
    'orders': paged_orders,
  }
  return render(request, 'manager/admin_orders.html', context)


# admin password change
@never_cache
@login_required(login_url='signin')
def admin_change_password(request):
  if request.method == 'POST':
    current_user = request.user
    current_password = request.POST['current_password']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    
    if password == confirm_password:
      if check_password(current_password, current_user.password):
        if check_password(password, current_user.password):
          messages.warning(request, 'Current password and new password is same')
        else:
          hashed_password = make_password(password)
          current_user.password = hashed_password
          current_user.save()
          messages.success(request, 'Password changed successfully')
      else:
        messages.error(request, 'Wrong password')
    else:
      messages.error(request, 'Passwords does not match')
  
  return render(request, 'manager/admin_password.html')