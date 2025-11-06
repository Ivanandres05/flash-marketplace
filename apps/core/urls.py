from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='home'),
    path('health/', views.health, name='health'),
    
    # Panel de administración
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    
    # Páginas de información
    path('about/', views.about, name='about'),
    path('careers/', views.careers, name='careers'),
    path('news/', views.news, name='news'),
    path('affiliate/', views.affiliate_program, name='affiliate'),
    path('payment-methods/', views.payment_methods, name='payment-methods'),
    path('customer-service/', views.customer_service, name='customer-service'),
    path('returns/', views.returns, name='returns'),
    path('shipping/', views.shipping_info, name='shipping'),
]