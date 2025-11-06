from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.catalog.models import Product, Category

def health(request):
    return JsonResponse({"status": "ok", "service": "flash", "version": "0.1.0"})

def index(request):
    """Homepage con productos destacados"""
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(available=True)[:8]
    best_sellers = Product.objects.filter(available=True).order_by('-created')[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'best_sellers': best_sellers,
    }
    return render(request, 'home.html', context)

# Páginas de información
def about(request):
    """Información corporativa"""
    return render(request, 'core/about.html')

def careers(request):
    """Trabaja con nosotros"""
    return render(request, 'core/careers.html')

def news(request):
    """Noticias"""
    return render(request, 'core/news.html')

def affiliate_program(request):
    """Programa de afiliados"""
    return render(request, 'core/affiliate.html')

def payment_methods(request):
    """Información sobre métodos de pago"""
    return render(request, 'core/payment_methods.html')

def customer_service(request):
    """Servicio al cliente"""
    return render(request, 'core/customer_service.html')

def returns(request):
    """Política de devoluciones"""
    return render(request, 'core/returns.html')

def shipping_info(request):
    """Información de envío"""
    return render(request, 'core/shipping.html')


# Panel de Administración
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Panel de control para administradores"""
    from django.contrib.auth.models import User
    from apps.accounts.models import Seller
    from apps.orders.models import Order, Coupon, CouponUsage
    from apps.reviews.models import Review
    
    # Fechas para filtros
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)
    
    # ========== USUARIOS ==========
    total_users = User.objects.count()
    new_users_month = User.objects.filter(date_joined__gte=last_30_days).count()
    new_users_week = User.objects.filter(date_joined__gte=last_7_days).count()
    active_users = User.objects.filter(is_active=True).count()
    
    # ========== VENDEDORES ==========
    total_sellers = Seller.objects.filter(is_verified=True).count()
    pending_sellers = Seller.objects.filter(is_verified=False).count()
    new_sellers_month = Seller.objects.filter(created_at__gte=last_30_days).count()
    
    # ========== VENTAS ==========
    total_orders = Order.objects.count()
    orders_month = Order.objects.filter(created_at__gte=last_30_days)
    orders_week = Order.objects.filter(created_at__gte=last_7_days)
    
    # Ventas por estado
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    canceled_orders = Order.objects.filter(status='canceled').count()
    
    # Ingresos
    total_revenue = Order.objects.filter(
        status__in=['delivered', 'shipped', 'processing']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    revenue_month = orders_month.filter(
        status__in=['delivered', 'shipped', 'processing']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    revenue_week = orders_week.filter(
        status__in=['delivered', 'shipped', 'processing']
    ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
    
    # Ticket promedio
    avg_order_value = Order.objects.filter(
        status__in=['delivered', 'shipped', 'processing']
    ).aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0')
    
    # ========== COMISIONES ==========
    # Flash cobra 10% de comisión sobre cada venta
    commission_rate = Decimal('0.10')
    total_commissions = total_revenue * commission_rate
    commissions_month = revenue_month * commission_rate
    commissions_week = revenue_week * commission_rate
    
    # ========== PRODUCTOS ==========
    total_products = Product.objects.count()
    active_products = Product.objects.filter(available=True).count()
    out_of_stock = Product.objects.filter(stock=0).count()
    low_stock = Product.objects.filter(stock__lte=10, stock__gt=0).count()
    
    # ========== CUPONES ==========
    total_coupons = Coupon.objects.count()
    active_coupons = Coupon.objects.filter(is_active=True).count()
    total_coupon_uses = CouponUsage.objects.count()
    coupon_uses_month = CouponUsage.objects.filter(used_at__gte=last_30_days).count()
    
    # Descuentos otorgados
    total_discounts = Order.objects.aggregate(
        total=Sum('discount_amount')
    )['total'] or Decimal('0')
    
    # ========== RESEÑAS/QUEJAS ==========
    total_reviews = Review.objects.count()
    pending_reviews = 0  # El modelo Review no tiene campo is_approved
    reviews_month = Review.objects.filter(created_at__gte=last_30_days).count()
    
    # Calificación promedio
    avg_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Reseñas por calificación
    reviews_5_star = Review.objects.filter(rating=5).count()
    reviews_4_star = Review.objects.filter(rating=4).count()
    reviews_3_star = Review.objects.filter(rating=3).count()
    reviews_2_star = Review.objects.filter(rating=2).count()
    reviews_1_star = Review.objects.filter(rating=1).count()
    
    # ========== CATEGORÍAS ==========
    total_categories = Category.objects.count()
    
    # Top 5 categorías por ventas
    from apps.orders.models import OrderItem
    top_categories = Category.objects.annotate(
        sales_count=Count('products__orderitem')
    ).order_by('-sales_count')[:5]
    
    # ========== PRODUCTOS MÁS VENDIDOS ==========
    top_products = Product.objects.annotate(
        sales_count=Count('orderitem')
    ).order_by('-sales_count')[:10]
    
    # ========== VENDEDORES TOP ==========
    # Obtener vendedores con sus usuarios
    from django.db.models import Prefetch
    top_sellers = Seller.objects.annotate(
        sales_count=Count('user__products__orderitem')
    ).filter(is_verified=True).order_by('-sales_count')[:10]
    
    # ========== ÓRDENES RECIENTES ==========
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:10]
    
    # ========== CUPONES MÁS USADOS ==========
    top_coupons = Coupon.objects.annotate(
        usage_count=Count('usages')
    ).order_by('-usage_count')[:5]
    
    context = {
        # Usuarios
        'total_users': total_users,
        'new_users_month': new_users_month,
        'new_users_week': new_users_week,
        'active_users': active_users,
        
        # Vendedores
        'total_sellers': total_sellers,
        'pending_sellers': pending_sellers,
        'new_sellers_month': new_sellers_month,
        
        # Ventas
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'canceled_orders': canceled_orders,
        
        # Ingresos
        'total_revenue': total_revenue,
        'revenue_month': revenue_month,
        'revenue_week': revenue_week,
        'avg_order_value': avg_order_value,
        
        # Comisiones
        'total_commissions': total_commissions,
        'commissions_month': commissions_month,
        'commissions_week': commissions_week,
        'commission_rate_percent': commission_rate * 100,
        
        # Productos
        'total_products': total_products,
        'active_products': active_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        
        # Cupones
        'total_coupons': total_coupons,
        'active_coupons': active_coupons,
        'total_coupon_uses': total_coupon_uses,
        'coupon_uses_month': coupon_uses_month,
        'total_discounts': total_discounts,
        
        # Reseñas
        'total_reviews': total_reviews,
        'pending_reviews': pending_reviews,
        'reviews_month': reviews_month,
        'avg_rating': avg_rating,
        'reviews_5_star': reviews_5_star,
        'reviews_4_star': reviews_4_star,
        'reviews_3_star': reviews_3_star,
        'reviews_2_star': reviews_2_star,
        'reviews_1_star': reviews_1_star,
        
        # Categorías
        'total_categories': total_categories,
        'top_categories': top_categories,
        
        # Top lists
        'top_products': top_products,
        'top_sellers': top_sellers,
        'recent_orders': recent_orders,
        'top_coupons': top_coupons,
    }
    
    return render(request, 'core/admin_dashboard.html', context)