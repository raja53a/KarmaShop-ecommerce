from .models import Cart,CartItem
from .views import _session_id
def cart_count(request):
    count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_session_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                count += cart_item.quantity
        except Cart.DoesNotExist:
            count = 0
    return dict(count=count)