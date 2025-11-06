from django.urls import path
from . import views
from apps.reviews import views as review_views

app_name = 'catalog'

urlpatterns = [
    path('', views.product_list_view, name='product-list'),
    path('<slug:slug>/', views.product_detail_view, name='product-detail'),
    path('<slug:slug>/review/', review_views.create_review, name='create-review'),
]
