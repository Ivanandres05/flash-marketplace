from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    
    # Cupones
    path('cupones/validar/', views.validate_coupon, name='validate_coupon'),
    path('cupones/eliminar/', views.remove_coupon, name='remove_coupon'),
    path('mis-cupones/', views.my_coupons, name='my_coupons'),
]