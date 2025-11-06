from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from apps.accounts.models import Seller
from apps.catalog.models import Product, Category
from apps.orders.models import Order, OrderItem
from decimal import Decimal

@login_required
def become_seller(request):
    """Registro como vendedor"""
    # Verificar si ya es vendedor
    if hasattr(request.user, 'seller_profile'):
        messages.info(request, 'Ya eres vendedor.')
        return redirect('seller:dashboard')
    
    if request.method == 'POST':
        store_name = request.POST.get('store_name', '').strip()
        description = request.POST.get('description', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        if not store_name:
            messages.error(request, 'El nombre de la tienda es obligatorio.')
            return render(request, 'seller/become_seller.html')
        
        # Verificar nombre único
        if Seller.objects.filter(store_name=store_name).exists():
            messages.error(request, 'Este nombre de tienda ya está en uso.')
            return render(request, 'seller/become_seller.html')
        
        # Crear perfil de vendedor
        Seller.objects.create(
            user=request.user,
            store_name=store_name,
            description=description,
            phone=phone
        )
        
        messages.success(request, f'¡Felicidades! Ahora eres vendedor. Bienvenido a {store_name}.')
        return redirect('seller:dashboard')
    
    return render(request, 'seller/become_seller.html')

@login_required
def seller_dashboard(request):
    """Dashboard principal del vendedor"""
    # Verificar que sea vendedor
    if not hasattr(request.user, 'seller_profile'):
        messages.warning(request, 'Primero debes registrarte como vendedor.')
        return redirect('seller:become')
    
    seller = request.user.seller_profile
    
    # Estadísticas
    products = Product.objects.filter(seller=request.user)
    total_products = products.count()
    active_products = products.filter(available=True).count()
    
    # Órdenes (items vendidos por este vendedor)
    order_items = OrderItem.objects.filter(product__seller=request.user)
    total_sales = order_items.aggregate(
        total=Sum('quantity')
    )['total'] or 0
    
    total_revenue = sum(
        item.product.price * item.quantity for item in order_items
    )
    
    # Últimos productos
    recent_products = products.order_by('-created')[:5]
    
    # Últimas ventas
    recent_sales = order_items.select_related('order', 'product').order_by('-order__created_at')[:10]
    
    context = {
        'seller': seller,
        'total_products': total_products,
        'active_products': active_products,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'recent_products': recent_products,
        'recent_sales': recent_sales,
    }
    
    return render(request, 'seller/dashboard.html', context)

@login_required
def seller_products(request):
    """Lista de productos del vendedor"""
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become')
    
    products = Product.objects.filter(seller=request.user).order_by('-created')
    
    context = {
        'products': products,
        'seller': request.user.seller_profile,
    }
    
    return render(request, 'seller/products.html', context)

@login_required
def create_product(request):
    """Crear nuevo producto"""
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_id = request.POST.get('category')
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        images = request.FILES.getlist('images')
        
        # Validaciones
        if not all([name, category_id, description, price, stock]):
            messages.error(request, 'Todos los campos son obligatorios.')
            categories = Category.objects.all()
            return render(request, 'seller/product_form.html', {'categories': categories})
        
        try:
            category = Category.objects.get(id=category_id)
            price = Decimal(price)
            stock = int(stock)
            
            # Generar slug único
            from django.utils.text import slugify
            base_slug = slugify(name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Crear producto
            product = Product.objects.create(
                seller=request.user,
                category=category,
                name=name,
                slug=slug,
                description=description,
                price=price,
                stock=stock,
                available=True
            )
            
            # Guardar imágenes
            from apps.catalog.models import ProductImage
            for image in images:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    alt_text=name
                )
            
            messages.success(request, f'Producto "{name}" creado exitosamente.')
            return redirect('seller:products')
            
        except Exception as e:
            messages.error(request, f'Error al crear producto: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'seller/product_form.html', {'categories': categories})

@login_required
def edit_product(request, product_id):
    """Editar producto existente"""
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name)
        product.description = request.POST.get('description', product.description)
        product.price = Decimal(request.POST.get('price', product.price))
        product.stock = int(request.POST.get('stock', product.stock))
        product.available = request.POST.get('available') == 'on'
        
        category_id = request.POST.get('category')
        if category_id:
            product.category = Category.objects.get(id=category_id)
        
        product.save()
        
        # Manejar nuevas imágenes
        new_images = request.FILES.getlist('images')
        if new_images:
            from apps.catalog.models import ProductImage
            for image in new_images:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    alt_text=product.name
                )
        
        # Eliminar imágenes seleccionadas
        images_to_delete = request.POST.getlist('delete_images')
        if images_to_delete:
            from apps.catalog.models import ProductImage
            ProductImage.objects.filter(id__in=images_to_delete, product=product).delete()
        
        messages.success(request, f'Producto "{product.name}" actualizado.')
        return redirect('seller:products')
    
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
        'editing': True,
    }
    return render(request, 'seller/product_form.html', context)

@login_required
def delete_product(request, product_id):
    """Eliminar producto"""
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become')
    
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Producto "{name}" eliminado.')
        return redirect('seller:products')
    
    return render(request, 'seller/delete_confirm.html', {'product': product})

@login_required
def seller_sales(request):
    """Historial de ventas del vendedor"""
    if not hasattr(request.user, 'seller_profile'):
        return redirect('seller:become')
    
    # Obtener todos los items de órdenes de productos del vendedor
    order_items = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related('order', 'product').order_by('-order__created_at')
    
    # DEBUG: Mostrar todos los OrderItems y sus productos con seller
    all_order_items = OrderItem.objects.all().select_related('product', 'order')
    debug_info = []
    for item in all_order_items:
        debug_info.append({
            'order_id': item.order.id,
            'product': item.product.name,
            'seller': item.product.seller.username if item.product.seller else 'Sin vendedor',
            'current_user': request.user.username,
            'match': item.product.seller == request.user if item.product.seller else False
        })
    
    # Calcular totales
    total_sales = sum(item.quantity for item in order_items)
    total_revenue = sum(item.product.price * item.quantity for item in order_items)
    
    context = {
        'order_items': order_items,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'seller': request.user.seller_profile,
        'debug_info': debug_info,  # Información de depuración
    }
    
    return render(request, 'seller/sales.html', context)
