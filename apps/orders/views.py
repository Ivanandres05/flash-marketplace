from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, Coupon, CouponUsage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from io import BytesIO
from datetime import datetime

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

def create_order(request):
    if request.method == 'POST':
        # Logic to create an order
        return HttpResponse("Order created!")
    return render(request, 'orders/create_order.html')

def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        # Logic to update the order
        return HttpResponse("Order updated!")
    return render(request, 'orders/update_order.html', {'order': order})

def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return HttpResponse("Order deleted!")

@login_required
def download_invoice(request, order_id):
    """Genera y descarga la factura en PDF con diseño profesional mejorado"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    
    # Contenedor de elementos
    elements = []
    
    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # ========== ENCABEZADO SUPERIOR ==========
    # Barra azul superior
    header_bar = Table([['']], colWidths=[7.5*inch], rowHeights=[8])
    header_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
    ]))
    elements.append(header_bar)
    elements.append(Spacer(1, 25))
    
    # Título y información de factura lado a lado
    title_style = ParagraphStyle(
        'CompanyTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        alignment=TA_LEFT,
    )
    
    invoice_style = ParagraphStyle(
        'InvoiceInfo',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#374151'),
        alignment=TA_RIGHT,
    )
    
    header_info = [
        [
            Paragraph("FLASH MARKETPLACE", title_style),
            Paragraph(f"<b>Factura N°:</b> FAC-{order.id:06d}<br/><b>Fecha:</b> {order.created_at.strftime('%d/%m/%Y')}<br/><b>Estado:</b> {order.get_status_display()}", invoice_style)
        ]
    ]
    
    header_table = Table(header_info, colWidths=[4*inch, 3.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(header_table)
    
    # Info de la empresa
    company_style = ParagraphStyle(
        'CompanyInfo',
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_LEFT,
    )
    
    company_text = Paragraph(
        "NIT: 900.123.456-7<br/>"
        "Calle Principal #123, Ciudad<br/>"
        "Tel: +57 (1) 234 5678 | Email: ventas@flashmarket.com",
        company_style
    )
    elements.append(company_text)
    elements.append(Spacer(1, 25))
    
    # ========== INFORMACIÓN DEL CLIENTE Y ENVÍO ==========
    section_style = ParagraphStyle(
        'SectionTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.white,
        alignment=TA_LEFT,
    )
    
    info_style = ParagraphStyle(
        'InfoText',
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#374151'),
        leading=14,
    )
    
    # Cliente y Envío en dos columnas
    client_name = order.user.get_full_name() or order.user.username
    
    cliente_box = [
        [Paragraph("DATOS DEL CLIENTE", section_style)],
        [Paragraph(f"<b>Nombre:</b> {client_name}<br/><b>Email:</b> {order.user.email}<br/><b>Teléfono:</b> {order.shipping_phone}", info_style)]
    ]
    
    envio_box = [
        [Paragraph("DIRECCIÓN DE ENVÍO", section_style)],
        [Paragraph(f"{order.shipping_address}<br/>{order.shipping_city}, {order.shipping_state}<br/>Código Postal: {order.shipping_zip_code}", info_style)]
    ]
    
    client_table = Table(cliente_box, colWidths=[3.5*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#3b82f6')),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#3b82f6')),
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
        ('TOPPADDING', (0, 0), (0, 0), 8),
        ('BOTTOMPADDING', (0, 0), (0, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (0, 1), 10),
        ('BOTTOMPADDING', (0, 1), (0, 1), 10),
    ]))
    
    envio_table = Table(envio_box, colWidths=[3.5*inch])
    envio_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#3b82f6')),
        ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#3b82f6')),
        ('INNERGRID', (0, 0), (-1, -1), 0, colors.white),
        ('TOPPADDING', (0, 0), (0, 0), 8),
        ('BOTTOMPADDING', (0, 0), (0, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (0, 1), 10),
        ('BOTTOMPADDING', (0, 1), (0, 1), 10),
    ]))
    
    info_boxes = [[client_table, envio_table]]
    info_table = Table(info_boxes, colWidths=[3.7*inch, 3.8*inch], spaceBefore=0, spaceAfter=0)
    info_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 25))
    
    # ========== TABLA DE PRODUCTOS ==========
    products_title = Paragraph("DETALLE DE PRODUCTOS", section_style)
    products_title_table = Table([[products_title]], colWidths=[7.5*inch])
    products_title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3b82f6')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(products_title_table)
    
    # Productos
    products_data = [
        ["PRODUCTO", "CANT.", "PRECIO UNIT.", "SUBTOTAL"]
    ]
    
    order_items = order.items.all()
    for item in order_items:
        products_data.append([
            item.product.name[:50],
            str(item.quantity),
            f"${item.price:,.0f}",
            f"${item.get_total():,.0f}"
        ])
    
    products_table = Table(products_data, colWidths=[4*inch, 0.8*inch, 1.3*inch, 1.4*inch])
    products_table.setStyle(TableStyle([
        # Encabezado
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#60a5fa')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        
        # Contenido
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#3b82f6')),
    ]))
    elements.append(products_table)
    elements.append(Spacer(1, 20))
    
    # ========== TOTALES ==========
    totals_data = [
        ["Subtotal:", f"${order.subtotal:,.0f}"],
        ["Envío:", f"${order.shipping_cost:,.0f}"],
        ["IVA (19%):", f"${order.tax:,.0f}"],
    ]
    
    totals_table = Table(totals_data, colWidths=[5.5*inch, 2*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#6b7280')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (1, 0), (1, -1), 12),
    ]))
    elements.append(totals_table)
    
    # Total final
    total_final = [
        ["TOTAL A PAGAR:", f"${order.total_amount:,.0f}"]
    ]
    
    total_table = Table(total_final, colWidths=[5.5*inch, 2*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (1, 0), (1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#1e40af')),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 20))
    
    # ========== MÉTODO DE PAGO ==========
    payment_text = Paragraph(
        f"<b>Método de Pago:</b> {order.get_payment_method_display()}",
        ParagraphStyle('PaymentText', fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#374151'))
    )
    payment_box = Table([[payment_text]], colWidths=[7.5*inch])
    payment_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f3f4f6')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(payment_box)
    elements.append(Spacer(1, 30))
    
    # ========== FOOTER ==========
    footer_style = ParagraphStyle(
        'Footer',
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER,
        leading=13,
    )
    
    footer_text = Paragraph(
        "<i>¡Gracias por tu compra en Flash Marketplace!</i><br/>"
        "Si tienes alguna pregunta sobre tu pedido, contáctanos:<br/>"
        "soporte@flashmarket.com | Tel: +57 (1) 234 5678",
        footer_style
    )
    elements.append(footer_text)
    elements.append(Spacer(1, 15))
    
    # Barra azul inferior
    footer_bar = Table([['']], colWidths=[7.5*inch], rowHeights=[5])
    footer_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
    ]))
    elements.append(footer_bar)
    
    # Generar PDF
    doc.build(elements)
    
    # Obtener el valor del buffer y crear la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_Flash_{order.id:06d}.pdf"'
    response.write(pdf)
    
    return response


# ==================== FUNCIONES DE CUPONES ====================

@login_required
def validate_coupon(request):
    """Valida y aplica un cupón al carrito (AJAX)"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Cupón no válido'
            })
        
        # Verificar si está autenticado
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'Debes iniciar sesión para usar cupones'
            })
        
        # Verificar si el usuario puede usar el cupón
        can_use, message = coupon.can_be_used_by(request.user)
        if not can_use:
            return JsonResponse({
                'success': False,
                'message': message
            })
        
        # Obtener el subtotal del carrito
        from apps.cart.models import Cart
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return JsonResponse({
                'success': False,
                'message': 'Tu carrito está vacío'
            })
        
        subtotal = cart.get_total()
        
        if subtotal == 0:
            return JsonResponse({
                'success': False,
                'message': 'Tu carrito está vacío'
            })
        
        # Verificar compra mínima
        if subtotal < coupon.min_purchase_amount:
            return JsonResponse({
                'success': False,
                'message': f'Compra mínima requerida: ${coupon.min_purchase_amount:,.0f}'
            })
        
        # Calcular descuento
        discount = coupon.calculate_discount(subtotal)
        new_total = subtotal - discount
        
        # Guardar cupón en sesión
        request.session['coupon_id'] = coupon.id
        request.session['discount_amount'] = float(discount)
        
        return JsonResponse({
            'success': True,
            'message': f'¡Cupón aplicado! Ahorras ${discount:,.0f}',
            'discount': float(discount),
            'new_total': float(new_total),
            'coupon_code': coupon.code
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def remove_coupon(request):
    """Elimina el cupón aplicado al carrito"""
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    if 'discount_amount' in request.session:
        del request.session['discount_amount']
    
    return JsonResponse({
        'success': True,
        'message': 'Cupón eliminado'
    })


@login_required
def my_coupons(request):
    """Muestra los cupones disponibles para el usuario"""
    from django.utils import timezone
    
    # Cupones disponibles (activos, no expirados, con usos disponibles)
    now = timezone.now()
    available_coupons = Coupon.objects.filter(
        is_active=True,
        valid_from__lte=now,
        valid_to__gte=now
    )
    
    # Filtrar por límite de uso del usuario
    coupons_with_status = []
    for coupon in available_coupons:
        can_use, message = coupon.can_be_used_by(request.user)
        coupons_with_status.append({
            'coupon': coupon,
            'can_use': can_use,
            'message': message
        })
    
    # Cupones ya usados por el usuario
    used_coupons = CouponUsage.objects.filter(user=request.user).select_related('coupon', 'order')
    
    context = {
        'coupons': coupons_with_status,
        'used_coupons': used_coupons
    }
    
    return render(request, 'orders/my_coupons.html', context)