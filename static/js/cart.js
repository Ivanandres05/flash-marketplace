// Obtener el CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Agregar producto al carrito
function addToCart(productId) {
    const quantity = document.getElementById('quantity') ? document.getElementById('quantity').value : 1;
    
    fetch(`/carrito/agregar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `quantity=${quantity}`
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Error al agregar el producto');
        }
    })
    .then(data => {
        // Solo actualizar el contador silenciosamente, sin notificación
        console.log('Producto agregado al carrito');
        
        // Actualizar contador del carrito
        updateCartCount();
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al agregar el producto', 'error');
    });
}

// Actualizar cantidad en el carrito
function updateQuantity(productId, change) {
    console.log('=== FUNCIÓN updateQuantity DE cart.js ===');
    console.log('Product ID:', productId, 'Change:', change);
    
    // Intentar encontrar el input por ID (usado en cart.html)
    let input = document.getElementById(`qty-${productId}`);
    
    // Si no existe, intentar por data-product-id (otros templates)
    if (!input) {
        input = document.querySelector(`input[data-product-id="${productId}"]`);
    }
    
    if (!input) {
        console.error('No se encontró el input para producto', productId);
        return;
    }
    
    const currentQty = parseInt(input.value);
    const newQty = currentQty + change;
    
    console.log('Cantidad actual:', currentQty, 'Nueva cantidad:', newQty);
    
    if (newQty < 1) {
        if (confirm('¿Deseas eliminar este producto del carrito?')) {
            removeItem(productId);
        }
        return;
    }
    
    // Actualizar visualmente primero
    input.value = newQty;
    
    fetch(`/carrito/actualizar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ quantity: newQty })
    })
    .then(response => {
        console.log('Respuesta:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Datos:', data);
        if (data.success) {
            // Recargar la página para actualizar totales
            location.reload();
        } else {
            console.error('Error del servidor:', data.message);
            alert('Error: ' + data.message);
            input.value = currentQty; // Revertir
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al actualizar la cantidad: ' + error);
        input.value = currentQty; // Revertir
    });
}

// Eliminar producto del carrito
function removeItem(productId) {
    fetch(`/carrito/eliminar/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al eliminar el producto', 'error');
    });
}

// Actualizar contador del carrito en el header
function updateCartCount() {
    fetch('/carrito/', {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        // Extraer el contador del HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const badge = doc.querySelector('.badge');
        if (badge) {
            const currentBadge = document.querySelector('.badge');
            if (currentBadge) {
                currentBadge.textContent = badge.textContent;
            }
        }
    })
    .catch(error => {
        console.error('Error al actualizar contador:', error);
    });
}

// Mostrar notificaciones
function showNotification(message, type = 'success') {
    // Crear el elemento de notificación
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 250px;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease-out;
    `;
    
    notification.innerHTML = `
        <strong>${type === 'success' ? '✓' : '✗'}</strong> ${message}
    `;
    
    document.body.appendChild(notification);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Agregar estilos para las animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
