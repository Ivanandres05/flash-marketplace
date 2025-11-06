from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'created_at', 'updated_at', 'status')
    search_fields = ('id', 'status')
    list_filter = ('status',)
    ordering = ('-created_at',)