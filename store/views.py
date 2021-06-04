from django.contrib import messages
from store.forms import ReviewForm
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from category.models import Category
from .models import Brand, Product, ProductGallery, ReviewRating
from category.models import Category
from django.db.models import Count
from carts.views import _session_id
from carts.models import CartItem
from django.core.paginator import Paginator
from orders.models import OrderProduct
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
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    
    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery':product_gallery,
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


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.full_name = form.cleaned_data['full_name']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted')
                return redirect(url)