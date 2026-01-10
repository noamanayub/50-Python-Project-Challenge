// Delivery option change
document.querySelectorAll('input[name="delivery"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const fees = { standard: 15, express: 35, pickup: 0 };
        const fee = fees[this.value];
        document.getElementById('deliveryFeeAmount').textContent = fee === 0 ? 'Free' : `$${fee.toFixed(2)}`;
        updateTotal();
    });
});

// Payment method change
document.querySelectorAll('input[name="payment"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const cardDetails = document.getElementById('cardDetails');
        cardDetails.style.display = this.value === 'card' ? 'block' : 'none';
    });
});

// Update total
function updateTotal() {
    const subtotal = 358;
    const serviceFee = 10;
    const deliveryFee = parseFloat(document.getElementById('deliveryFeeAmount').textContent.replace('$', '').replace('Free', '0'));
    const tax = (subtotal + deliveryFee + serviceFee) * 0.08;
    const total = subtotal + deliveryFee + serviceFee + tax;
    
    document.getElementById('totalAmount').textContent = `$${total.toFixed(2)}`;
}

// Place order
function placeOrder() {
    const agreeTerms = document.getElementById('agreeTerms');
    
    if (!agreeTerms.checked) {
        showNotification('Please agree to the Terms & Conditions', 'error');
        return;
    }
    
    // Validate form fields
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    let allValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            allValid = false;
            field.style.borderColor = '#b21900';
        } else {
            field.style.borderColor = '#e0e0e0';
        }
    });
    
    if (!allValid) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }
    
    // Show loading
    const btn = document.querySelector('.btn-place-order');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    btn.disabled = true;
    
    // Simulate order processing
    setTimeout(() => {
        showNotification('Order placed successfully! Redirecting...', 'success');
        
        setTimeout(() => {
            // Clear cart and redirect
            localStorage.removeItem('renthub_checkout');
            window.location.href = '../account/account.html';
        }, 2000);
    }, 2000);
}

// Card number formatting
document.querySelector('input[placeholder="1234 5678 9012 3456"]')?.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s/g, '');
    let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
    e.target.value = formattedValue;
});

// Expiry date formatting
document.querySelector('input[placeholder="MM/YY"]')?.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    e.target.value = value;
});

// Notification system
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const colors = { success: '#28a745', error: '#b21900', warning: '#ffc107', info: '#173641' };
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `position:fixed;top:20px;right:20px;padding:15px 25px;background-color:${colors[type]};color:white;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:10000;animation:slideIn 0.3s ease;font-weight:500;max-width:350px;`;
    
    const style = document.createElement('style');
    style.textContent = '@keyframes slideIn{from{transform:translateX(400px);opacity:0}to{transform:translateX(0);opacity:1}}@keyframes slideOut{from{transform:translateX(0);opacity:1}to{transform:translateX(400px);opacity:0}}';
    if (!document.querySelector('style[data-notif]')) {
        style.setAttribute('data-notif', 'true');
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Load checkout data
document.addEventListener('DOMContentLoaded', function() {
    const checkoutData = localStorage.getItem('renthub_checkout');
    if (checkoutData) {
        // You can populate form with saved data here
        console.log('Checkout data loaded:', JSON.parse(checkoutData));
    }
});
