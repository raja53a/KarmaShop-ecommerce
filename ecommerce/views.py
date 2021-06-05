from django.shortcuts import render
from store.models   import Product, HomeContent, BrandLogo
def home(request):
    homecontent = HomeContent.objects.all()
    brandlogo = BrandLogo.objects.all()
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products' : products,  'homecontent':homecontent, 'brandlogo': brandlogo
    }
    return render(request, 'home.html',context)