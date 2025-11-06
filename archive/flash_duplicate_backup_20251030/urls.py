from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('catalog/', include('apps.catalog.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('search/', include('apps.search.urls')),
]