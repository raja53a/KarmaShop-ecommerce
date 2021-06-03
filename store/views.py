from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Brand, Product
from category.models import Category
from django.db.models import Count
from carts.views import _session_id
from carts.models import CartItem
from django.core.paginator import Paginator
# Create your views here.
def shop(request, category_slug=None):
    categories        = None
    products        = None
    if category_slug != None:
        categories   = get_object_or_404(Category, slug=category_slug)
        products     = Product.objects.filter(product_category=categories,is_available=True)
        paginator      = Paginator(products,6)
        page           = request.GET.get('page')
        paged_products = paginator.get_page(page)
        search_count = products.count()
    else:
        products       = Product.objects.all().filter(is_available=True).order_by('id')
        paginator      = Paginator(products,6)
        page           = request.GET.get('page')
        paged_products = paginator.get_page(page)
        search_count = products.count()

    categorylist    = Category.objects.annotate(total_products=Count('product'))
    brandlist       = Brand.objects.annotate(total_brands=Count('product'))
    context = {
        'category_list' : categorylist, 'brandlist': brandlist, 'products' : paged_products,
        'search_count' : search_count, 
    }
    return render(request,'shop/shop.html',context)

def product_detail(request,category_slug,product_slug):
    try:
        category_slug   = get_object_or_404(Category, slug=category_slug)
        single_product = Product.objects.get(product_category=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_session_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request,'shop/product_detail.html',context)

def search(request):
    categorylist    = Category.objects.annotate(total_products=Count('product'))
    brandlist       = Brand.objects.annotate(total_brands=Count('product'))
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            search_count = products.count()
    context = {
        'products' : products, 'search_count':search_count, 'category_list':categorylist, 'brandlist':brandlist
    }
    return render(request,'shop/shop.html',context)