from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, Coupon, CouponUsage

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'coupon', 'discount_amount', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('user__username', 'id', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'subtotal', 'discount_amount', 'shipping_cost', 'tax', 'total_amount')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('user', 'status', 'created_at', 'updated_at')
        }),
        ('Dirección de Envío', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_phone')
        }),
        ('Pago y Descuentos', {
            'fields': ('payment_method', 'subtotal', 'coupon', 'discount_amount', 'shipping_cost', 'tax', 'total_amount')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Order, OrderAdmin)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_display', 'validity_status', 'usage_status', 'is_active', 'valid_from', 'valid_to')
    list_filter = ('is_active', 'discount_type', 'valid_from', 'valid_to')
    search_fields = ('code', 'description')
    readonly_fields = ('times_used', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Descuento', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Validez', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Restricciones', {
            'fields': ('min_purchase_amount', 'usage_limit', 'usage_limit_per_user', 'times_used')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def discount_display(self, obj):
        """Muestra el descuento de forma visual"""
        if obj.discount_type == 'percentage':
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">'
                '{}% OFF</span>',
                obj.discount_value
            )
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">'
            '${:,.0f} COP OFF</span>',
            obj.discount_value
        )
    discount_display.short_description = 'Descuento'
    
    def validity_status(self, obj):
        """Muestra el estado de validez del cupón"""
        is_valid, message = obj.is_valid()
        if is_valid:
            return format_html(
                '<span style="color: green;">✓ Válido</span>'
            )
        return format_html(
            '<span style="color: orange;" title="{}">⏳ {}</span>',
            message, message[:30]
        )
    validity_status.short_description = 'Estado'
    
    def usage_status(self, obj):
        """Muestra el uso del cupón"""
        if not obj.usage_limit:
            return format_html('<span style="color: gray;">Sin límite</span>')
        
        percentage = (obj.times_used / obj.usage_limit) * 100
        color = '#28a745' if percentage < 50 else '#ffc107' if percentage < 80 else '#dc3545'
        
        return format_html(
            '<span style="color: {};">{} / {}</span>',
            color, obj.times_used, obj.usage_limit
        )
    usage_status.short_description = 'Uso'


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'order', 'used_at')
    list_filter = ('used_at', 'coupon')
    search_fields = ('user__username', 'coupon__code', 'order__id')
    readonly_fields = ('coupon', 'user', 'order', 'used_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False