from django.urls import path
from apps.accounts import seller_views

app_name = 'seller'

urlpatterns = [
    path('convertirse-vendedor/', seller_views.become_seller, name='become'),
    path('dashboard/', seller_views.seller_dashboard, name='dashboard'),
    path('productos/', seller_views.seller_products, name='products'),
    path('productos/crear/', seller_views.create_product, name='create-product'),
    path('productos/<int:product_id>/editar/', seller_views.edit_product, name='edit-product'),
    path('productos/<int:product_id>/eliminar/', seller_views.delete_product, name='delete-product'),
    path('ventas/', seller_views.seller_sales, name='sales'),
]
