from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    
    # Frontend URLs
    path('', include('apps.core.urls')),
    path('productos/', include('apps.catalog.urls')),
    path('carrito/', include('apps.cart.urls')),
    path('cuenta/', include('apps.accounts.urls')),
    path('vendedor/', include('apps.accounts.seller_urls')),
    path('pedidos/', include(('apps.orders.urls', 'orders'), namespace='orders')),
    path('resenas/', include('apps.reviews.urls')),
    # path('cupones/', include('apps.coupons.urls')),  # TODO: Activar después de migrar
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)