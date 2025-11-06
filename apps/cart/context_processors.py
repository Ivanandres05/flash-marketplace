from apps.cart.models import CartItem, Cart

def cart_counter(request):
    """Context processor para mostrar cantidad de items en el carrito"""
    cart_count = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = CartItem.objects.filter(cart=cart).count()
        except Cart.DoesNotExist:
            cart_count = 0
    else:
        # Para usuarios anónimos
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, user__isnull=True)
                cart_count = CartItem.objects.filter(cart=cart).count()
            except Cart.DoesNotExist:
                cart_count = 0
    
    return {
        'cart_count': cart_count
    }
