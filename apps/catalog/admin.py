from django.contrib import admin
from .models import Product, Category, ProductImage

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'available')
    search_fields = ('name', 'description')
    list_filter = ('category', 'available')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)