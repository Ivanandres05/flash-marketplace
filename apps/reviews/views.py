from django.shortcuts import render, get_object_or_404
from .models import Review
from django.http import JsonResponse

def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def create_review(request, slug):
    """Crear una reseña para un producto (desde el detalle de producto)."""
    if request.method == 'POST':
        rating = int(request.POST.get('rating') or 0)
        comment = request.POST.get('comment', '').strip()

        # Validaciones basicas
        if rating < 1 or rating > 5:
            messages.error(request, 'Selecciona una calificación válida (1-5).')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Crear la review
        from apps.catalog.models import Product

        product = Product.objects.filter(slug=slug).first()
        if not product:
            messages.error(request, 'Producto no encontrado.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Evitar duplicados: un usuario puede reseñar una vez (si prefieres permitir varias, cambia esto)
        existing = Review.objects.filter(product=product, user=request.user).first()
        if existing:
            existing.rating = rating
            existing.comment = comment
            existing.save()
            messages.success(request, 'Tu reseña ha sido actualizada.')
        else:
            Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
            messages.success(request, '¡Gracias! Tu reseña ha sido agregada.')

        return redirect('catalog:product-detail', slug=product.slug)

    # Si no es POST redirigimos al home
    return redirect('catalog:product-list')

def update_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        # Logic to update the review
        pass
    return render(request, 'reviews/update_review.html', {'review': review})

def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return JsonResponse({'success': True})
    return render(request, 'reviews/delete_review.html', {'review': review})