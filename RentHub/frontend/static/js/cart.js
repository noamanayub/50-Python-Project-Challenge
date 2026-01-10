// Cart data - Load from localStorage or start empty
let cartItems = JSON.parse(localStorage.getItem('renthub_cart')) || [];

const deliveryFee = 15;
const serviceFee = 10;
let discountAmount = 0;

// Save cart to localStorage
function saveCart() {
    localStorage.setItem('renthub_cart', JSON.stringify(cartItems));
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    renderCartItems();
    updateTotals();
    initializeDates();
});

// Initialize rental dates
function initializeDates() {
    const today = new Date();
    const startDateInput = document.getElementById('startDate');
    const returnDateInput = document.getElementById('returnDate');
    
    startDateInput.min = today.toISOString().split('T')[0];
    startDateInput.value = today.toISOString().split('T')[0];
    
    startDateInput.addEventListener('change', function() {
        updateReturnDate();
    });
    
    updateReturnDate();
}

function updateReturnDate() {
    if (cartItems.length === 0) return;
    const startDate = new Date(document.getElementById('startDate').value);
    const maxDays = Math.max(...cartItems.map(item => item.days));
    const returnDate = new Date(startDate);
    returnDate.setDate(returnDate.getDate() + maxDays);
    
    document.getElementById('returnDate').value = returnDate.toISOString().split('T')[0];
}

// Get category-specific image
function getCategoryImage(category) {
    const images = {
        'Electronics': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=150',
        'Vehicles': 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=150',
        'Furniture': 'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=150',
        'Tools': 'https://images.unsplash.com/photo-1586920740099-44f76d89c44b?w=150',
        'Gaming': 'https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=150',
        'Fashion': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=150',
        'Tools & Equipment': 'https://images.unsplash.com/photo-1586920740099-44f76d89c44b?w=150',
        'Default': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=150'
    };
    return images[category] || images['Default'];
}

// Render cart items dynamically
function renderCartItems() {
    const cartItemsList = document.getElementById('cartItemsList');
    const emptyCart = document.getElementById('emptyCart');
    
    if (cartItems.length === 0) {
        if (cartItemsList) cartItemsList.style.display = 'none';
        if (emptyCart) emptyCart.style.display = 'block';
        return;
    }
    
    if (cartItemsList) {
        cartItemsList.style.display = 'block';
        cartItemsList.innerHTML = '';
        
        cartItems.forEach((item, index) => {
            const price = parseFloat(item.price.replace('$', '')) || 0;
            const quantity = item.quantity || 1;
            const days = item.days || 1;
            const total = price * quantity;
            const imageUrl = item.image || getCategoryImage(item.category);
            
            const cartItemHTML = `
                <div class="cart-item" data-id="${item.id}">
                    <div class="item-image">
                        <img src="${imageUrl}" alt="${item.title}">
                    </div>
                    <div class="item-details">
                        <h3>${item.title}</h3>
                        <p class="item-category">${item.category || 'General'}</p>
                        <div class="item-features">
                            <span><i class="fas fa-check"></i> Available</span>
                        </div>
                    </div>
                    <div class="item-rental-period">
                        <label>Rental Period:</label>
                        <select class="rental-select" onchange="updateItemPrice(this, ${item.id})">
                            <option value="1" ${days === 1 ? 'selected' : ''}>1 Day - $${price}</option>
                            <option value="3" ${days === 3 ? 'selected' : ''}>3 Days - $${(price * 2.5).toFixed(0)}</option>
                            <option value="7" ${days === 7 ? 'selected' : ''}>1 Week - $${(price * 5).toFixed(0)}</option>
                            <option value="30" ${days === 30 ? 'selected' : ''}>1 Month - $${(price * 18).toFixed(0)}</option>
                        </select>
                    </div>
                    <div class="item-quantity">
                        <label>Qty:</label>
                        <div class="quantity-control">
                            <button onclick="decreaseQuantity(${item.id})">-</button>
                            <input type="number" value="${quantity}" min="1" id="qty-${item.id}" onchange="updateQuantity(${item.id})">
                            <button onclick="increaseQuantity(${item.id})">+</button>
                        </div>
                    </div>
                    <div class="item-price">
                        <span class="price-label">Total:</span>
                        <span class="price" id="price-${item.id}">$${total.toFixed(2)}</span>
                    </div>
                    <button class="remove-item" onclick="removeItem(${item.id})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            cartItemsList.innerHTML += cartItemHTML;
        });
    }
    
    if (emptyCart) emptyCart.style.display = 'none';
}

// Update item price based on rental period
function updateItemPrice(select, itemId) {
    const selectedOption = select.options[select.selectedIndex];
    const days = parseInt(select.value);
    const priceText = selectedOption.text;
    const price = parseFloat(priceText.match(/\$(\d+)/)[1]);
    
    const item = cartItems.find(i => i.id === itemId);
    if (item) {
        item.days = days;
        item.price = price;
        item.basePrice = price / days;
    }
    
    updateItemTotal(itemId);
    updateTotals();
    updateReturnDate();
    saveCart();
}

// Quantity controls
function increaseQuantity(itemId) {
    const input = document.getElementById(`qty-${itemId}`);
    input.value = parseInt(input.value) + 1;
    updateQuantity(itemId);
}

function decreaseQuantity(itemId) {
    const input = document.getElementById(`qty-${itemId}`);
    if (parseInt(input.value) > 1) {
        input.value = parseInt(input.value) - 1;
        updateQuantity(itemId);
    }
}

function updateQuantity(itemId) {
    const input = document.getElementById(`qty-${itemId}`);
    const quantity = parseInt(input.value);
    
    if (quantity < 1) {
        input.value = 1;
        return;
    }
    
    const item = cartItems.find(i => i.id === itemId);
    if (item) {
        item.quantity = quantity;
    }
    
    updateItemTotal(itemId);
    updateTotals();
    saveCart();
}

// Update individual item total
function updateItemTotal(itemId) {
    const item = cartItems.find(i => i.id === itemId);
    if (item) {
        const price = typeof item.price === 'string' ? parseFloat(item.price.replace('$', '')) : item.price;
        const total = price * (item.quantity || 1);
        const priceElement = document.getElementById(`price-${itemId}`);
        if (priceElement) {
            priceElement.textContent = `$${total.toFixed(2)}`;
        }
    }
}

// Calculate totals
function updateTotals() {
    const subtotal = cartItems.reduce((sum, item) => {
        const price = typeof item.price === 'string' ? parseFloat(item.price.replace('$', '')) : item.price;
        return sum + (price * (item.quantity || 1));
    }, 0);
    
    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('deliveryFee').textContent = `$${deliveryFee.toFixed(2)}`;
    document.getElementById('serviceFee').textContent = `$${serviceFee.toFixed(2)}`;
    
    if (discountAmount > 0) {
        document.getElementById('discountRow').style.display = 'flex';
        document.getElementById('discount').textContent = `-$${discountAmount.toFixed(2)}`;
    }
    
    const total = subtotal + deliveryFee + serviceFee - discountAmount;
    document.getElementById('total').textContent = `$${total.toFixed(2)}`;
    
    updateItemCount();
}

// Update item count
function updateItemCount() {
    const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('itemCount').textContent = totalItems;
}

// Remove item
function removeItem(itemId) {
    if (confirm('Remove this item from cart?')) {
        const itemIndex = cartItems.findIndex(i => i.id === itemId);
        if (itemIndex > -1) {
            cartItems.splice(itemIndex, 1);
            document.querySelector(`[data-id="${itemId}"]`).remove();
            updateTotals();
            saveCart();
            
            showNotification('Item removed from cart', 'info');
            
            if (cartItems.length === 0) {
                showEmptyCart();
            }
        }
    }
}

// Clear cart
function clearCart() {
    if (confirm('Are you sure you want to clear your cart?')) {
        cartItems = [];
        localStorage.removeItem('renthub_cart');
        document.getElementById('cartItemsList').innerHTML = '';
        showEmptyCart();
        showNotification('Cart cleared', 'info');
    }
}

// Show empty cart
function showEmptyCart() {
    document.getElementById('cartItemsList').style.display = 'none';
    document.getElementById('emptyCart').style.display = 'block';
}

// Apply promo code
function applyPromo() {
    const promoInput = document.getElementById('promoInput');
    const promoCode = promoInput.value.trim().toUpperCase();
    
    const promoCodes = {
        'WELCOME10': 0.10,
        'SAVE20': 0.20,
        'FIRST30': 0.30
    };
    
    if (promoCodes[promoCode]) {
        const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        discountAmount = subtotal * promoCodes[promoCode];
        updateTotals();
        showNotification(`Promo code applied! You saved $${discountAmount.toFixed(2)}`, 'success');
        promoInput.value = '';
    } else {
        showNotification('Invalid promo code', 'error');
    }
}

// Proceed to checkout
function proceedToCheckout() {
    if (cartItems.length === 0) {
        showNotification('Your cart is empty', 'warning');
        return;
    }
    
    const startDate = document.getElementById('startDate').value;
    if (!startDate) {
        showNotification('Please select a start date', 'warning');
        return;
    }
    
    // Store checkout data
    const checkoutData = {
        items: cartItems,
        subtotal: cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0),
        deliveryFee: deliveryFee,
        serviceFee: serviceFee,
        discount: discountAmount,
        total: cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0) + deliveryFee + serviceFee - discountAmount,
        startDate: startDate,
        returnDate: document.getElementById('returnDate').value
    };
    
    localStorage.setItem('renthub_checkout', JSON.stringify(checkoutData));
    
    showNotification('Proceeding to checkout...', 'success');
    
    setTimeout(() => {
        window.location.href = '/checkout/';
    }, 1000);
}

// Recommended items add to cart
document.querySelectorAll('.btn-add-cart').forEach(button => {
    button.addEventListener('click', function() {
        const item = this.closest('.recommended-item');
        const name = item.querySelector('h4').textContent;
        showNotification(`${name} added to cart!`, 'success');
    });
});

// Notification system
function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background-color: ${getNotificationColor(type)};
        color: white;
        border-radius: 6px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
        max-width: 350px;
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
    `;
    
    if (!document.querySelector('style[data-notification]')) {
        style.setAttribute('data-notification', 'true');
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function getNotificationColor(type) {
    const colors = {
        success: '#28a745',
        error: '#b21900',
        warning: '#ffc107',
        info: '#173641'
    };
    return colors[type] || colors.info;
}
