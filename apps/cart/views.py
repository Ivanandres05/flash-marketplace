from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .models import Cart, CartItem
from apps.catalog.models import Product
from apps.accounts.models import Address

def get_or_create_cart(request):
    """Obtener o crear carrito para el usuario actual o sesión"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Para usuarios anónimos, usar sesión
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, user__isnull=True)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

def view_cart(request):
    """Vista del carrito de compras"""
    from decimal import Decimal
    from apps.orders.models import Coupon
    
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    
    # Calcular totales
    subtotal = sum(item.product.price * item.quantity for item in items)
    discount = Decimal('0')
    coupon = None
    coupon_error = None
    
    # Verificar si hay un cupón aplicado en la sesión
    if request.user.is_authenticated and 'coupon_id' in request.session:
        try:
            coupon = Coupon.objects.get(id=request.session['coupon_id'])
            can_use, message = coupon.can_be_used_by(request.user)
            
            if can_use and subtotal >= coupon.min_purchase_amount:
                discount = coupon.calculate_discount(subtotal)
            else:
                coupon_error = message if not can_use else f'Compra mínima: ${coupon.min_purchase_amount:,.0f} COP'
                coupon = None
                # Limpiar cupón inválido de la sesión
                del request.session['coupon_id']
                if 'discount_amount' in request.session:
                    del request.session['discount_amount']
        except Coupon.DoesNotExist:
            # Limpiar cupón inexistente de la sesión
            del request.session['coupon_id']
            if 'discount_amount' in request.session:
                del request.session['discount_amount']
    
    shipping = Decimal('0') if subtotal > 50000 else Decimal('5000')
    total = subtotal - discount + shipping
    
    context = {
        'cart_items': items,
        'subtotal': subtotal,
        'discount': discount,
        'coupon': coupon,
        'coupon_error': coupon_error,
        'shipping': shipping,
        'total': total,
    }
    
    return render(request, 'cart/cart.html', context)

@require_POST
def add_to_cart(request, product_id):
    """Agregar producto al carrito"""
    from django.http import JsonResponse
    
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        # Obtener cantidad desde JSON o POST tradicional
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error al parsear JSON: {e}")
                quantity = 1
        else:
            quantity = int(request.POST.get('quantity', 1))
        
        # Validar cantidad
        if quantity < 1:
            quantity = 1
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            if cart_item.quantity + quantity <= product.stock:
                cart_item.quantity += quantity
                cart_item.save()
                message = f'{product.name} agregado al carrito.'
                success = True
            else:
                message = f'No hay suficiente stock de {product.name}.'
                success = False
        else:
            message = f'{product.name} agregado al carrito.'
            success = True
        
        # Si es una petición AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            cart_count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
            return JsonResponse({
                'success': success,
                'message': message,
                'cart_count': cart_count
            })
        
        # Si no es AJAX, redirigir SIN mostrar ningún mensaje (ni éxito ni error)
        # No agregar ningún mensaje para evitar notificaciones molestas
        
        # Redirigir al carrito si se solicitó desde el detalle del producto
        if request.GET.get('redirect') == 'cart':
            return redirect('cart:view-cart')
        
        # De lo contrario, regresar a la página anterior
        return redirect(request.META.get('HTTP_REFERER', 'catalog:product-list'))
        
    except Exception as e:
        print(f"Error en add_to_cart: {e}")
        if request.content_type == 'application/json':
            return JsonResponse({
                'success': False,
                'message': f'Error al agregar al carrito: {str(e)}',
                'cart_count': 0
            }, status=500)
        else:
            messages.error(request, 'Error al agregar el producto al carrito.')
            return redirect(request.META.get('HTTP_REFERER', 'catalog:product-list'))

def update_cart(request, product_id):
    """Actualizar cantidad de producto en el carrito (AJAX)"""
    from django.http import JsonResponse
    
    if request.method == 'POST':
        try:
            # Intentar obtener quantity de POST data o JSON
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                quantity = int(data.get('quantity', 1))
            else:
                quantity = int(request.POST.get('quantity', 1))
            
            cart = get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
            
            if quantity > 0 and quantity <= cart_item.product.stock:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Carrito actualizado'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Cantidad no válida'
                }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
    return JsonResponse({'success': False}, status=400)

def remove_from_cart(request, product_id):
    """Eliminar producto del carrito"""
    if request.method == 'POST':
        cart = get_or_create_cart(request)
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            product_name = cart_item.product.name
            cart_item.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'{product_name} eliminado del carrito'
                })
            else:
                messages.success(request, f'{product_name} eliminado del carrito.')
                return redirect('cart:view-cart')
        except CartItem.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Producto no encontrado en el carrito'
                }, status=404)
            else:
                messages.error(request, 'Producto no encontrado en el carrito.')
                return redirect('cart:view-cart')
    return redirect('cart:view-cart')

@login_required
def checkout(request):
    """Vista de checkout"""
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    
    if not items.exists():
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('cart:view-cart')
    
    # Obtener direcciones guardadas del usuario
    saved_addresses = Address.objects.filter(user=request.user)
    
    # Calcular totales
    from decimal import Decimal
    from apps.orders.models import Coupon
    
    subtotal = sum(item.product.price * item.quantity for item in items)
    discount = Decimal('0')
    coupon = None
    
    # Verificar si hay un cupón aplicado en la sesión
    if request.user.is_authenticated and 'coupon_id' in request.session:
        try:
            coupon = Coupon.objects.get(id=request.session['coupon_id'])
            can_use, message = coupon.can_be_used_by(request.user)
            
            if can_use and subtotal >= coupon.min_purchase_amount:
                discount = coupon.calculate_discount(subtotal)
            else:
                # Limpiar cupón inválido de la sesión
                del request.session['coupon_id']
                if 'discount_amount' in request.session:
                    del request.session['discount_amount']
                coupon = None
        except Coupon.DoesNotExist:
            # Limpiar cupón inexistente de la sesión
            del request.session['coupon_id']
            if 'discount_amount' in request.session:
                del request.session['discount_amount']
    
    shipping = Decimal('0') if subtotal > 50000 else Decimal('5000')
    tax = (subtotal - discount) * Decimal('0.19')  # IVA 19% sobre subtotal después del descuento
    total = subtotal - discount + shipping + tax
    
    if request.method == 'POST':
        try:
            from apps.orders.models import Order, OrderItem
            
            # Obtener datos del formulario
            address_id = request.POST.get('address_id')
            payment_method = request.POST.get('payment_method', 'card')
            
            # Si se seleccionó una dirección guardada
            if address_id:
                address = Address.objects.get(id=address_id, user=request.user)
                shipping_address = address.street
                shipping_city = address.city
                shipping_state = address.state
                shipping_zip_code = address.zip_code
                shipping_phone = request.user.profile.phone_number if hasattr(request.user, 'profile') else ''
            else:
                # Nueva dirección
                shipping_address = request.POST.get('street', '')
                shipping_city = request.POST.get('city', '')
                shipping_state = request.POST.get('state', '')
                shipping_zip_code = request.POST.get('zip_code', '')
                shipping_phone = request.POST.get('phone', '')
            
            # Crear el pedido
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                shipping_city=shipping_city,
                shipping_state=shipping_state,
                shipping_zip_code=shipping_zip_code,
                shipping_phone=shipping_phone,
                payment_method=payment_method,
                subtotal=Decimal(str(subtotal)),
                shipping_cost=Decimal(str(shipping)),
                tax=Decimal(str(tax)),
                total_amount=Decimal(str(total)),
                status='pending',
                coupon=coupon,  # Agregar el cupón al pedido
                discount_amount=Decimal(str(discount))  # Agregar el descuento al pedido
            )
            
            # Crear los items del pedido
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                
                # Reducir el stock del producto
                item.product.stock -= item.quantity
                item.product.save()
            
            # Registrar el uso del cupón si se aplicó uno
            if coupon:
                from apps.orders.models import CouponUsage
                CouponUsage.objects.create(
                    coupon=coupon,
                    user=request.user,
                    order=order
                )
                # Incrementar el contador de veces usado
                coupon.times_used += 1
                coupon.save()
            
            # Limpiar carrito
            items.delete()
            
            # Limpiar cupón de la sesión
            if 'coupon_id' in request.session:
                del request.session['coupon_id']
            if 'discount_amount' in request.session:
                del request.session['discount_amount']
            
            messages.success(request, f'¡Pedido #{order.id} realizado con éxito! Te enviaremos un email de confirmación.')
            return redirect('accounts:profile')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pedido: {str(e)}')
            return redirect('cart:checkout')
    
    context = {
        'cart_items': items,
        'saved_addresses': saved_addresses,
        'subtotal': subtotal,
        'discount': discount,
        'coupon': coupon,
        'shipping': shipping,
        'tax': tax,
        'total': total,
    }
    
    return render(request, 'cart/checkout.html', context)
