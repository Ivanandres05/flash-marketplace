from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.utils import timezone
from .models import Profile, Address, PasswordResetCode

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        print(f"🔐 Intento de login - Usuario: {username}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"✓ Autenticación exitosa para: {username}")
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
        else:
            print(f"✗ Autenticación fallida para: {username}")
            # Verificar si el usuario existe
            from django.contrib.auth.models import User
            if User.objects.filter(username=username).exists():
                print(f"  - Usuario existe en BD, contraseña incorrecta")
                messages.error(request, 'Contraseña incorrecta')
            else:
                print(f"  - Usuario NO existe en BD")
                messages.error(request, 'Usuario no encontrado')
    
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validar campos vacíos
        if not all([username, email, first_name, last_name, password1, password2]):
            messages.error(request, 'Todos los campos son obligatorios')
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        # Validar longitud del username
        if len(username) < 4:
            messages.error(request, 'El nombre de usuario debe tener al menos 4 caracteres')
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        # Validaciones
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso')
            return render(request, 'accounts/register.html', {
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado')
            return render(request, 'accounts/register.html', {
                'username': username,
                'first_name': first_name,
                'last_name': last_name
            })
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
        
        try:
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            print(f"✓ Usuario creado: {username}")
            
            # Crear perfil
            Profile.objects.create(user=user)
            
            print(f"✓ Perfil creado para: {username}")
            
            # Iniciar sesión automáticamente
            # Re-autenticar después de crear el usuario para asegurar que funcione
            authenticated_user = authenticate(request, username=username, password=password1)
            
            if authenticated_user:
                login(request, authenticated_user)
                print(f"✓ Sesión iniciada para: {username}")
                messages.success(request, '¡Cuenta creada exitosamente! Bienvenido a Flash.')
                return redirect('core:home')
            else:
                print(f"✗ Error al autenticar después de crear usuario: {username}")
                messages.warning(request, 'Cuenta creada correctamente, pero hubo un problema al iniciar sesión. Por favor, inicia sesión manualmente.')
                return redirect('accounts:login')
        except Exception as e:
            print(f"✗ Error al crear usuario: {str(e)}")
            messages.error(request, f'Error al crear la cuenta: {str(e)}')
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            })
    
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    # Asegurarnos de que el usuario tenga un perfil
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    print(f"📊 Profile view - Usuario: {request.user.username}, Método: {request.method}")
    print(f"   Email alternativo actual en BD: '{profile.alternate_email}'")
    
    if request.method == 'POST':
        print(f"📝 POST recibido - Datos completos:")
        for key, value in request.POST.items():
            print(f"   {key}: '{value}'")
        
        # Actualizar información personal
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.save()
        
        # Actualizar correo alternativo en el perfil
        alternate_email = request.POST.get('alternate_email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        
        print(f"💾 Guardando perfil de {request.user.username}")
        print(f"   Email alternativo recibido: '{alternate_email}'")
        print(f"   Teléfono recibido: '{phone_number}'")
        print(f"   Email alternativo ANTES de guardar: '{profile.alternate_email}'")
        
        profile.alternate_email = alternate_email if alternate_email else None
        profile.phone_number = phone_number if phone_number else None
        
        try:
            profile.save()
            print(f"   ✅ Profile.save() ejecutado sin errores")
        except Exception as e:
            print(f"   ❌ ERROR al guardar profile: {type(e).__name__}: {e}")
        
        # Verificar que se guardó
        profile.refresh_from_db()
        print(f"   ✅ Email alternativo en BD DESPUÉS de guardar: '{profile.alternate_email}'")
        print(f"   ✅ Teléfono en BD DESPUÉS de guardar: '{profile.phone_number}'")
        
        messages.success(request, 'Información actualizada correctamente')
        return redirect('accounts:profile')
    
    # Obtener pedidos del usuario
    orders = []
    try:
        from apps.orders.models import Order
        orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    except:
        pass
    
    context = {
        'orders': orders,
        'profile': profile,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def my_orders(request):
    """Ver todos los pedidos del usuario"""
    # Asegurarnos de que el usuario tenga un perfil
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Obtener TODOS los pedidos del usuario
    orders = []
    try:
        from apps.orders.models import Order
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    except:
        pass
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'accounts/my_orders.html', context)

@login_required
def order_detail(request, order_id):
    """Ver detalle de un pedido específico"""
    from apps.orders.models import Order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'accounts/order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    """Cancelar un pedido"""
    from apps.orders.models import Order
    
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Solo se pueden cancelar pedidos pendientes o en proceso
        if order.status in ['pending', 'processing']:
            order.status = 'canceled'
            cancel_reason = request.POST.get('cancel_reason', '')
            if cancel_reason:
                order.notes = f"Cancelado por el usuario. Motivo: {cancel_reason}"
            else:
                order.notes = "Cancelado por el usuario."
            order.save()
            messages.success(request, f'Pedido #{order.id} cancelado exitosamente.')
        else:
            messages.error(request, 'No se puede cancelar este pedido en su estado actual.')
        
        return redirect('accounts:order-detail', order_id=order_id)
    
    return redirect('accounts:orders')

@login_required
def my_addresses(request):
    """Gestionar direcciones de envío"""
    addresses = Address.objects.filter(user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            Address.objects.create(
                user=request.user,
                street=request.POST.get('street_address'),  # Cambiado de street_address a street
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('zip_code')
            )
            messages.success(request, 'Dirección agregada correctamente')
        
        elif action == 'delete':
            address_id = request.POST.get('address_id')
            Address.objects.filter(id=address_id, user=request.user).delete()
            messages.success(request, 'Dirección eliminada')
        
        return redirect('accounts:addresses')
    
    return render(request, 'accounts/my_addresses.html', {'addresses': addresses})

@login_required
def delete_account(request):
    """Eliminar cuenta de usuario"""
    if request.method == 'POST':
        password = request.POST.get('password')
        
        # Verificar contraseña
        if request.user.check_password(password):
            username = request.user.username
            request.user.delete()
            messages.success(request, f'Tu cuenta "{username}" ha sido eliminada permanentemente.')
            return redirect('core:home')
        else:
            messages.error(request, 'Contraseña incorrecta. No se pudo eliminar la cuenta.')
            return redirect('accounts:delete-account')
    
    return render(request, 'accounts/delete_account.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('core:home')


# ========== RECUPERACIÓN DE CONTRASEÑA ==========

def request_password_reset(request):
    """Solicitar código de recuperación de contraseña"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()  # Puede ser email o username
        
        if not identifier:
            messages.error(request, 'Por favor ingresa tu correo electrónico o nombre de usuario.')
            return render(request, 'accounts/request_password_reset.html')
        
        try:
            # Buscar por email o username
            from django.db.models import Q
            user = User.objects.get(Q(email=identifier) | Q(username=identifier))
            
            print(f"🔍 Usuario encontrado: {user.username} ({user.email})")
            
            # Invalidar códigos anteriores no usados
            old_codes = PasswordResetCode.objects.filter(user=user, is_used=False).count()
            PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)
            print(f"🔄 Invalidados {old_codes} códigos antiguos")
            
            # Crear nuevo código
            reset_code = PasswordResetCode.objects.create(user=user)
            print(f"✓ Código creado: {reset_code.code}")
            
            # Determinar email de destino: usar email alternativo si existe
            try:
                profile = user.profile
                destination_email = profile.alternate_email if (profile.alternate_email and profile.alternate_email.strip()) else user.email
                print(f"📧 Email alternativo en BD: '{profile.alternate_email}'")
            except Exception as e:
                print(f"⚠️  Error al obtener profile: {e}")
                destination_email = user.email
            
            print(f"📧 Email de destino final: {destination_email} {'(alternativo)' if destination_email != user.email else '(principal)'}")
            
            # Capturar variables para el thread
            user_name = user.first_name or user.username
            user_email = user.email
            destination_email_thread = destination_email
            code = reset_code.code
            from_email = django_settings.DEFAULT_FROM_EMAIL
            
            print(f"📧 Preparando envío desde: {from_email} a {destination_email_thread}")
            
            # Preparar contenido del email
            subject = 'Código de Recuperación de Contraseña - Flash Marketplace'
            
            # Contenido del mensaje en HTML y texto plano
            html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
        .code-box {{ background-color: #f8f9fa; border: 2px solid #007bff; padding: 20px; margin: 20px 0; text-align: center; }}
        .code {{ font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #007bff; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Flash Marketplace</h1>
        </div>
        <h2>Recuperación de Contraseña</h2>
        <p>Hola <strong>{user_name}</strong>,</p>
        <p>Has solicitado restablecer tu contraseña en Flash Marketplace.</p>
        <div class="code-box">
            <p>Tu código de verificación es:</p>
            <div class="code">{code}</div>
        </div>
        <p><strong>Este código expirará en 15 minutos.</strong></p>
        <p>Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
        <div class="footer">
            <p>Saludos,<br>El equipo de Flash Marketplace</p>
        </div>
    </div>
</body>
</html>
            '''
            
            text_content = f'''
Hola {user_name},

Has solicitado restablecer tu contraseña en Flash Marketplace.

Tu código de verificación es: {code}

Este código expirará en 15 minutos.

Si no solicitaste este cambio, ignora este correo.

Saludos,
El equipo de Flash Marketplace
            '''
            
            print(f"\n{'='*60}")
            print(f"📧 ENVIANDO EMAIL CON DJANGO SMTP")
            print(f"{'='*60}")
            print(f"  - Desde: {from_email}")
            print(f"  - Para: {destination_email_thread}")
            print(f"  - Código: {code}")
            print(f"  - Backend: {django_settings.EMAIL_BACKEND}")
            
            # Usar send_mail de Django directamente (más confiable)
            from django.core.mail import EmailMultiAlternatives
            import socket
            
            # Configurar timeout más corto para evitar worker timeout
            socket.setdefaulttimeout(30)
            
            try:
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=from_email,
                    to=[destination_email_thread]
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
                
                print(f"✅ Email enviado exitosamente con Django!")
                print(f"{'='*60}\n")
            except socket.timeout:
                print(f"⚠️ TIMEOUT al enviar email (30s), pero código guardado")
                print(f"{'='*60}\n")
                # Continuar de todas formas, el código está guardado
            except Exception as e:
                print(f"\n❌ ERROR AL ENVIAR EMAIL:")
                print(f"   Tipo: {type(e).__name__}")
                print(f"   Mensaje: {str(e)}")
                print(f"{'='*60}\n")
                # Continuar de todas formas, el código está guardado
            finally:
                socket.setdefaulttimeout(None)
            
            # Guardar el identifier en la sesión para el siguiente paso
            request.session['reset_identifier'] = identifier
            
            # Mensaje personalizado según donde se envió
            if destination_email_thread != user_email:
                messages.success(request, f'Se ha enviado un código de verificación a tu correo alternativo: {destination_email_thread}')
            else:
                messages.success(request, f'Se ha enviado un código de verificación a tu correo: {destination_email_thread}')
            
            return redirect('accounts:verify-reset-code')
                
        except User.DoesNotExist:
            print(f"⚠️  Usuario no encontrado con email/username: {identifier}")
            # Por seguridad, no revelar si el usuario existe o no
            messages.success(request, f'Si el email o usuario está registrado, recibirás un código de verificación.')
            return redirect('accounts:verify-reset-code')
        except Exception as e:
            print(f"❌ ERROR CRÍTICO: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            messages.error(request, 'Ocurrió un error al procesar tu solicitud. Por favor intenta de nuevo.')
            return render(request, 'accounts/request_password_reset.html')
    
    return render(request, 'accounts/request_password_reset.html')


def verify_reset_code(request):
    """Verificar el código de recuperación"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Por favor solicita primero un código de recuperación')
        return redirect('accounts:request-password-reset')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        try:
            user = User.objects.get(email=email)
            from .models import PasswordResetCode
            from django.utils import timezone
            
            # Buscar código válido
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()
            
            if reset_code:
                # Código válido - guardar en sesión y redirigir
                request.session['reset_code_id'] = reset_code.id
                messages.success(request, 'Código verificado correctamente')
                return redirect('accounts:reset-password')
            else:
                messages.error(request, 'Código inválido o expirado')
                
        except User.DoesNotExist:
            messages.error(request, 'Error en la verificación')
            return redirect('accounts:request-password-reset')
    
    return render(request, 'accounts/verify_reset_code.html', {'email': email})


def reset_password(request):
    """Cambiar la contraseña con código verificado"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    reset_code_id = request.session.get('reset_code_id')
    if not reset_code_id:
        messages.error(request, 'Por favor verifica primero tu código')
        return redirect('accounts:verify-reset-code')
    
    if request.method == 'POST':
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'accounts/reset_password.html')
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return render(request, 'accounts/reset_password.html')
        
        try:
            from .models import PasswordResetCode
            reset_code = PasswordResetCode.objects.get(id=reset_code_id)
            
            if reset_code.is_valid():
                # Cambiar contraseña
                user = reset_code.user
                user.set_password(password1)
                user.save()
                
                # Marcar código como usado
                reset_code.is_used = True
                reset_code.save()
                
                # Limpiar sesión
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                if 'reset_code_id' in request.session:
                    del request.session['reset_code_id']
                
                messages.success(request, '¡Contraseña cambiada exitosamente! Ya puedes iniciar sesión.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'El código ha expirado o ya fue usado')
                return redirect('accounts:request-password-reset')
                
        except PasswordResetCode.DoesNotExist:
            messages.error(request, 'Error en la verificación')
            return redirect('accounts:request-password-reset')
    
    return render(request, 'accounts/reset_password.html')

@login_required
def payment_methods(request):
    """Gestionar métodos de pago del usuario"""
    from .models import PaymentMethod
    
    methods = PaymentMethod.objects.filter(user=request.user)
    
    return render(request, 'accounts/payment_methods.html', {
        'payment_methods': methods
    })

@login_required
@require_POST
def add_payment_method(request):
    """Agregar nuevo método de pago"""
    from .models import PaymentMethod
    
    try:
        card_type = request.POST.get('card_type', 'visa')
        card_holder = request.POST.get('card_holder', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        expiry_month = request.POST.get('expiry_month', '').strip()
        expiry_year = request.POST.get('expiry_year', '').strip()
        is_default = request.POST.get('is_default') == 'on'
        
        # Validaciones
        if not card_holder or not card_number or not expiry_month or not expiry_year:
            messages.error(request, 'Todos los campos son obligatorios')
            return redirect('accounts:payment-methods')
        
        if len(card_number) < 4:
            messages.error(request, 'Número de tarjeta inválido')
            return redirect('accounts:payment-methods')
        
        # Guardar solo los últimos 4 dígitos
        last_four = card_number[-4:]
        
        # Crear método de pago
        PaymentMethod.objects.create(
            user=request.user,
            card_type=card_type,
            card_holder=card_holder,
            card_number=last_four,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            is_default=is_default
        )
        
        messages.success(request, '✓ Tarjeta agregada exitosamente')
        
    except Exception as e:
        messages.error(request, f'Error al agregar tarjeta: {str(e)}')
    
    return redirect('accounts:payment-methods')

@login_required
@require_POST
def delete_payment_method(request, method_id):
    """Eliminar método de pago"""
    from .models import PaymentMethod
    
    try:
        method = PaymentMethod.objects.get(id=method_id, user=request.user)
        method.delete()
        messages.success(request, '✓ Tarjeta eliminada correctamente')
    except PaymentMethod.DoesNotExist:
        messages.error(request, 'Tarjeta no encontrada')
    except Exception as e:
        messages.error(request, f'Error al eliminar tarjeta: {str(e)}')
    
    return redirect('accounts:payment-methods')

@login_required
@require_POST
def set_default_payment(request, method_id):
    """Establecer método de pago como predeterminado"""
    from .models import PaymentMethod
    
    try:
        # Quitar default de todas las tarjetas del usuario
        PaymentMethod.objects.filter(user=request.user).update(is_default=False)
        
        # Establecer la seleccionada como default
        method = PaymentMethod.objects.get(id=method_id, user=request.user)
        method.is_default = True
        method.save()
        
        messages.success(request, '✓ Tarjeta predeterminada actualizada')
    except PaymentMethod.DoesNotExist:
        messages.error(request, 'Tarjeta no encontrada')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
    
    return redirect('accounts:payment-methods')

@login_required
def wishlist(request):
    """Ver lista de deseos del usuario"""
    from .models import Wishlist
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'accounts/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Agregar producto a la lista de deseos"""
    from .models import Wishlist
    from apps.catalog.models import Product
    from django.http import JsonResponse
    
    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'added': created,
                'message': 'Producto agregado a favoritos' if created else 'Producto ya estaba en favoritos'
            })
        
        if created:
            messages.success(request, f'{product.name} agregado a tu lista de deseos')
        else:
            messages.info(request, f'{product.name} ya estaba en tu lista de deseos')
        
        return redirect(request.META.get('HTTP_REFERER', 'accounts:wishlist'))
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'message': f'Error al agregar a favoritos: {str(e)}'
            }, status=500)
        messages.error(request, 'Error al agregar el producto a favoritos')
        return redirect(request.META.get('HTTP_REFERER', 'catalog:product-list'))

@login_required
def remove_from_wishlist(request, product_id):
    """Eliminar producto de la lista de deseos"""
    from .models import Wishlist
    from django.http import JsonResponse
    
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Producto eliminado de favoritos'})
    
    messages.success(request, 'Producto eliminado de tu lista de deseos')
    return redirect('accounts:wishlist')

@login_required
def my_reviews(request):
    """Ver reseñas escritas por el usuario"""
    return render(request, 'accounts/my_reviews.html')

@login_required
def settings(request):
    """Configuración de cuenta"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Actualizar preferencias de notificaciones
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.order_notifications = request.POST.get('order_notifications') == 'on'
        profile.promotional_notifications = request.POST.get('promotional_notifications') == 'on'
        profile.save()
        
        messages.success(request, 'Configuración actualizada correctamente')
        return redirect('accounts:settings')
    
    return render(request, 'accounts/settings.html', {'profile': profile})

@login_required
def change_password(request):
    """Cambiar contraseña del usuario"""
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Verificar contraseña actual
        if not request.user.check_password(current_password):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('accounts:change-password')
        
        # Verificar que las contraseñas nuevas coincidan
        if new_password != confirm_password:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
            return redirect('accounts:change-password')
        
        # Verificar longitud mínima
        if len(new_password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('accounts:change-password')
        
        # Cambiar contraseña
        request.user.set_password(new_password)
        request.user.save()
        
        # Mantener la sesión activa
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Contraseña actualizada correctamente')
        return redirect('accounts:settings')
    
    return render(request, 'accounts/change_password.html')

def password_reset_request(request):
    """Solicitar restablecimiento de contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Por favor ingresa tu correo electrónico')
            return render(request, 'accounts/password_reset.html')
        
        try:
            user = User.objects.get(email=email)
            
            # Generar token seguro
            from django.contrib.auth.tokens import default_token_generator
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.core.mail import send_mail
            from django.template.loader import render_to_string
            from django.conf import settings
            
            # Crear token y uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Construir URL de reset
            reset_url = request.build_absolute_uri(
                f'/cuenta/restablecer/{uid}/{token}/'
            )
            
            # Preparar contexto para el email
            context = {
                'user': user,
                'reset_url': reset_url,
                'site_name': 'Flash Marketplace',
            }
            
            # Renderizar email HTML
            html_message = render_to_string('accounts/email/password_reset_email.html', context)
            plain_message = f"""
Hola {user.first_name or user.username},

Has solicitado restablecer tu contraseña en Flash Marketplace.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 24 horas.

Si no solicitaste este cambio, ignora este mensaje.

Saludos,
Equipo Flash Marketplace
            """.strip()
            
            # Enviar email
            try:
                send_mail(
                    subject='Recuperación de Contraseña - Flash Marketplace',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                messages.success(
                    request, 
                    f'✉️ Se ha enviado un enlace de recuperación a {email}. '
                    'Revisa tu bandeja de entrada y spam.'
                )
                print(f"📧 Email de recuperación enviado a: {email}")
                print(f"🔗 URL de reset (para testing): {reset_url}")
                
            except Exception as e:
                print(f"❌ Error enviando email: {e}")
                messages.warning(
                    request,
                    f'Email enviado a {email}. Si tienes problemas, contacta a soporte.'
                )
            
            return redirect('accounts:login')
            
        except User.DoesNotExist:
            # Por seguridad, no revelar que el email no existe
            messages.success(
                request,
                f'Si existe una cuenta con {email}, recibirás un email con instrucciones.'
            )
            return redirect('accounts:login')
    
    return render(request, 'accounts/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    """Confirmar y establecer nueva contraseña"""
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    
    # Validar token
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Verificar si el token es válido
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            # Validaciones
            if not password or not confirm_password:
                messages.error(request, 'Por favor completa ambos campos')
                return render(request, 'accounts/password_reset_confirm.html', {
                    'validlink': True,
                    'uidb64': uidb64,
                    'token': token,
                })
            
            if password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden')
                return render(request, 'accounts/password_reset_confirm.html', {
                    'validlink': True,
                    'uidb64': uidb64,
                    'token': token,
                })
            
            if len(password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                return render(request, 'accounts/password_reset_confirm.html', {
                    'validlink': True,
                    'uidb64': uidb64,
                    'token': token,
                })
            
            # Establecer nueva contraseña
            user.set_password(password)
            user.save()
            
            messages.success(
                request, 
                '✓ Contraseña restablecida correctamente. Ya puedes iniciar sesión.'
            )
            print(f"🔐 Contraseña restablecida para: {user.username}")
            return redirect('accounts:login')
        
        # GET request - mostrar formulario
        return render(request, 'accounts/password_reset_confirm.html', {
            'validlink': True,
            'uidb64': uidb64,
            'token': token,
        })
    else:
        # Token inválido o expirado
        messages.error(
            request,
            'El enlace de recuperación es inválido o ha expirado. '
            'Por favor solicita uno nuevo.'
        )
        return redirect('accounts:password-reset')
