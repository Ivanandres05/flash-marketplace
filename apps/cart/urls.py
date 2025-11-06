from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view-cart'),
    path('agregar/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('actualizar/<int:product_id>/', views.update_cart, name='update-cart'),
    path('eliminar/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
]