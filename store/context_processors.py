from .models import CartItem, Cart


def cart_context(request):
    """
    Context processor to make cart count available in all templates.
    """
    cart_count = 0
    
    try:
        if request.user.is_authenticated:
            cart_count = CartItem.objects.filter(user=request.user, is_active=True).count()
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                try:
                    cart = Cart.objects.get(cart_id=cart_id)
                    cart_count = CartItem.objects.filter(cart=cart, is_active=True).count()
                except Cart.DoesNotExist:
                    pass
    except:
        pass
    
    return {
        'cart_count': cart_count,
    }
