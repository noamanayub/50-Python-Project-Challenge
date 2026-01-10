// Image Gallery
function changeImage(thumbnail) {
    document.getElementById('mainImage').src = thumbnail.src.replace('w=150', 'w=600');
    document.querySelectorAll('.thumbnail-gallery img').forEach(img => img.classList.remove('active'));
    thumbnail.classList.add('active');
}

// Quantity controls
function increaseQty() {
    const input = document.getElementById('quantity');
    input.value = parseInt(input.value) + 1;
}

function decreaseQty() {
    const input = document.getElementById('quantity');
    if (parseInt(input.value) > 1) input.value = parseInt(input.value) - 1;
}

// Price update
function updatePrice() {
    const select = document.getElementById('rentalPeriod');
    const selectedText = select.options[select.selectedIndex].text;
    const price = selectedText.match(/\$(\d+)/)[1];
    document.querySelector('.price').textContent = '$' + price;
}

// Tabs
function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Rent Now
function rentNow() {
    showNotification('Processing rental...', 'success');
    setTimeout(() => window.location.href = '/checkout/', 1000);
}

// Add to Cart
function addToCart() {
    showNotification('Added to cart!', 'success');
}

// Wishlist toggle
document.querySelector('.wishlist-btn').addEventListener('click', function() {
    const icon = this.querySelector('i');
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        this.style.backgroundColor = '#b21900';
        this.style.color = '#fff';
        showNotification('Added to wishlist!', 'success');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        this.style.backgroundColor = '#fff';
        this.style.color = '#666';
        showNotification('Removed from wishlist', 'info');
    }
});

// Initialize date
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    document.getElementById('startDate').min = today.toISOString().split('T')[0];
    document.getElementById('startDate').value = today.toISOString().split('T')[0];
});

// Notification
function showNotification(message, type = 'info') {
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `position:fixed;top:20px;right:20px;padding:15px 25px;background-color:${type==='success'?'#28a745':type==='error'?'#b21900':'#173641'};color:white;border-radius:6px;box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:10000;animation:slideIn 0.3s ease;font-weight:500;`;
    
    const style = document.createElement('style');
    style.textContent = '@keyframes slideIn{from{transform:translateX(400px);opacity:0}to{transform:translateX(0);opacity:1}}';
    if (!document.querySelector('style[data-notif]')) {
        style.setAttribute('data-notif', 'true');
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}
