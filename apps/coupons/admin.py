from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Coupon, CouponUsage


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'discount_display', 'validity_status', 'usage_status', 'is_active', 'created_at')
    list_filter = ('is_active', 'discount_type', 'created_at', 'valid_from', 'valid_to')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('times_used', 'created_at', 'updated_at')
    filter_horizontal = ('specific_users',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('code', 'name', 'description', 'is_active')
        }),
        ('Descuento', {
            'fields': ('discount_type', 'discount_value', 'maximum_discount')
        }),
        ('Validez', {
            'fields': ('valid_from', 'valid_to')
        }),
        ('Restricciones', {
            'fields': ('minimum_purchase', 'usage_limit', 'usage_limit_per_user', 'times_used')
        }),
        ('Usuarios Específicos', {
            'fields': ('specific_users',),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return format_html('<strong>{}%</strong> OFF', obj.discount_value)
        else:
            return format_html('<strong>${:,.0f}</strong> COP OFF', obj.discount_value)
    discount_display.short_description = 'Descuento'
    
    def validity_status(self, obj):
        now = timezone.now()
        if obj.valid_from > now:
            return format_html('<span style="color: orange;">⏳ Próximamente</span>')
        elif obj.valid_to < now:
            return format_html('<span style="color: red;">❌ Expirado</span>')
        else:
            return format_html('<span style="color: green;">✅ Vigente</span>')
    validity_status.short_description = 'Vigencia'
    
    def usage_status(self, obj):
        if obj.usage_limit:
            percentage = (obj.times_used / obj.usage_limit) * 100
            if percentage >= 100:
                color = 'red'
            elif percentage >= 75:
                color = 'orange'
            else:
                color = 'green'
            return format_html(
                '<span style="color: {};">{} / {}</span>',
                color, obj.times_used, obj.usage_limit
            )
        return format_html('<span style="color: green;">{} (Ilimitado)</span>', obj.times_used)
    usage_status.short_description = 'Usos'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    list_filter = ('used_at', 'coupon')
    search_fields = ('user__username', 'coupon__code', 'order__id')
    readonly_fields = ('coupon', 'user', 'order', 'discount_amount', 'used_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
