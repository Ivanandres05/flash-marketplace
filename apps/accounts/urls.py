from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('pedidos/', views.my_orders, name='orders'),
    path('pedidos/<int:order_id>/', views.order_detail, name='order-detail'),
    path('pedidos/<int:order_id>/cancelar/', views.cancel_order, name='cancel-order'),
    path('direcciones/', views.my_addresses, name='addresses'),
    path('metodos-pago/', views.payment_methods, name='payment-methods'),
    path('metodos-pago/agregar/', views.add_payment_method, name='add-payment-method'),
    path('metodos-pago/eliminar/<int:method_id>/', views.delete_payment_method, name='delete-payment-method'),
    path('metodos-pago/predeterminada/<int:method_id>/', views.set_default_payment, name='set-default-payment'),
    path('lista-deseos/', views.wishlist, name='wishlist'),
    path('lista-deseos/agregar/<int:product_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('lista-deseos/eliminar/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('mis-resenas/', views.my_reviews, name='my-reviews'),
    path('configuracion/', views.settings, name='settings'),
    path('cambiar-contrasena/', views.change_password, name='change-password'),
    
    # Recuperación de contraseña con código por email
    path('solicitar-recuperacion/', views.request_password_reset, name='request-password-reset'),
    path('verificar-codigo/', views.verify_reset_code, name='verify-reset-code'),
    path('restablecer-contrasena/', views.reset_password, name='reset-password'),
    
    # URLs antiguas (mantener para compatibilidad)
    path('recuperar-contrasena/', views.password_reset_request, name='password-reset'),
    path('restablecer/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),
    path('eliminar-cuenta/', views.delete_account, name='delete-account'),
]