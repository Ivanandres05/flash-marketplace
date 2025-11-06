from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Coupon, CouponUsage
from apps.cart.models import Cart
from decimal import Decimal


@login_required
@require_POST
def validate_coupon(request):
    """
    Validar un cupón y aplicarlo al carrito
    POST /cupones/validar/
    Body: {"code": "FLASH10"}
    """
    code = request.POST.get('code', '').strip().upper()
    
    if not code:
        return JsonResponse({
            'success': False,
            'message': 'Por favor ingresa un código de cupón'
        })
    
    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Cupón no válido'
        })
    
    # Obtener el carrito del usuario
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return JsonResponse({
            'success': False,
            'message': 'Tu carrito está vacío'
        })
    
    # Calcular subtotal
    subtotal = sum(item.subtotal for item in cart.items.all())
    
    # Aplicar cupón
    result = coupon.apply_to_order(Decimal(str(subtotal)), request.user)
    
    if result['success']:
        # Guardar cupón en sesión
        request.session['coupon_code'] = code
        request.session['coupon_discount'] = str(result['discount'])
        
        return JsonResponse({
            'success': True,
            'message': result['message'],
            'discount': float(result['discount']),
            'final_total': float(result['final_total']),
            'coupon_info': {
                'code': coupon.code,
                'name': coupon.name,
                'type': coupon.get_discount_type_display(),
                'value': str(coupon.discount_value)
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'message': result['message']
        })


@login_required
@require_POST
def remove_coupon(request):
    """
    Remover cupón del carrito
    POST /cupones/remover/
    """
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    
    return JsonResponse({
        'success': True,
        'message': 'Cupón removido'
    })


@login_required
def my_coupons(request):
    """
    Listar cupones disponibles para el usuario
    GET /cupones/mis-cupones/
    """
    from django.utils import timezone
    now = timezone.now()
    
    # Cupones públicos activos
    public_coupons = Coupon.objects.filter(
        is_active=True,
        valid_from__lte=now,
        valid_to__gte=now
    ).filter(
        models.Q(specific_users__isnull=True) | models.Q(specific_users=request.user)
    ).distinct()
    
    # Cupones ya usados por el usuario
    used_coupons = CouponUsage.objects.filter(user=request.user).select_related('coupon')
    
    # Filtrar cupones que el usuario puede usar
    available_coupons = []
    for coupon in public_coupons:
        can_use, message = coupon.can_be_used_by(request.user)
        if can_use:
            available_coupons.append(coupon)
    
    context = {
        'available_coupons': available_coupons,
        'used_coupons': used_coupons,
    }
    
    return render(request, 'coupons/my_coupons.html', context)


def apply_coupon_to_session(request, code):
    """
    Función helper para aplicar cupón desde cualquier parte
    """
    try:
        coupon = Coupon.objects.get(code=code.upper())
        
        # Obtener carrito
        from apps.cart.models import Cart
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return False, "Carrito vacío"
        
        subtotal = sum(item.subtotal for item in cart.items.all())
        result = coupon.apply_to_order(Decimal(str(subtotal)), request.user)
        
        if result['success']:
            request.session['coupon_code'] = code.upper()
            request.session['coupon_discount'] = str(result['discount'])
            return True, result['message']
        
        return False, result['message']
    except Coupon.DoesNotExist:
        return False, "Cupón no válido"


def get_session_coupon(request):
    """
    Obtener información del cupón en sesión
    """
    code = request.session.get('coupon_code')
    discount = request.session.get('coupon_discount')
    
    if code and discount:
        try:
            coupon = Coupon.objects.get(code=code)
            return {
                'code': code,
                'discount': Decimal(discount),
                'coupon': coupon
            }
        except Coupon.DoesNotExist:
            # Limpiar sesión si el cupón ya no existe
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
            if 'coupon_discount' in request.session:
                del request.session['coupon_discount']
    
    return None


from django.db import models
