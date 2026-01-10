// ===========================
// Shopping Cart Functionality
// ===========================
let cart = [];
let wishlist = [];

// Initialize cart from localStorage
function initCart() {
    const savedCart = localStorage.getItem('renthub_cart');
    const savedWishlist = localStorage.getItem('renthub_wishlist');
    
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCartBadge();
    }
    
    if (savedWishlist) {
        wishlist = JSON.parse(savedWishlist);
    }
}

// Update cart badge
function updateCartBadge() {
    const badge = document.querySelector('.badge');
    if (badge) {
        badge.textContent = cart.length;
    }
}

// Add to cart
function addToCart(item) {
    cart.push(item);
    localStorage.setItem('renthub_cart', JSON.stringify(cart));
    updateCartBadge();
    showNotification('Item added to cart!', 'success');
}

// Toggle wishlist
function toggleWishlist(itemId) {
    const index = wishlist.indexOf(itemId);
    
    if (index > -1) {
        wishlist.splice(index, 1);
        showNotification('Removed from wishlist', 'info');
    } else {
        wishlist.push(itemId);
        showNotification('Added to wishlist!', 'success');
    }
    
    localStorage.setItem('renthub_wishlist', JSON.stringify(wishlist));
}

// ===========================
// Search Functionality
// ===========================
const searchInput = document.getElementById('searchInput');
const searchBtn = document.querySelector('.search-btn');

if (searchBtn) {
    searchBtn.addEventListener('click', performSearch);
}

if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
}

function performSearch() {
    const query = searchInput.value.trim();
    
    if (query) {
        showNotification(`Searching for: ${query}`, 'info');
        // Here you would typically send a request to your backend
        console.log('Searching for:', query);
    } else {
        showNotification('Please enter a search term', 'warning');
    }
}

// ===========================
// Rent Now Buttons
// ===========================
document.addEventListener('DOMContentLoaded', function() {
    initCart();
    
    // Add click handlers to all "Rent Now" buttons
    const rentButtons = document.querySelectorAll('.btn-rent');
    
    rentButtons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productCard = this.closest('.product-card');
            const productTitle = productCard.querySelector('.product-title').textContent;
            const productPrice = productCard.querySelector('.price').textContent;
            const productCategory = productCard.querySelector('.product-category').textContent;
            
            const item = {
                id: Date.now() + index,
                title: productTitle,
                price: productPrice,
                category: productCategory
            };
            
            addToCart(item);
        });
    });
    
    // Add click handlers to wishlist buttons
    const wishlistButtons = document.querySelectorAll('.wishlist-btn');
    
    wishlistButtons.forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productCard = this.closest('.product-card');
            const productTitle = productCard.querySelector('.product-title').textContent;
            const icon = this.querySelector('i');
            
            // Toggle icon
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                this.style.backgroundColor = '#b21900';
                this.style.color = '#fff';
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                this.style.backgroundColor = '#fff';
                this.style.color = '#666';
            }
            
            toggleWishlist(productTitle);
        });
    });
    
    // Category card click handlers
    const categoryCards = document.querySelectorAll('.category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const categoryName = this.querySelector('h3').textContent;
            showNotification(`Browsing ${categoryName} category`, 'info');
        });
    });
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    
    if (newsletterForm) {
        const newsletterBtn = newsletterForm.querySelector('button');
        const newsletterInput = newsletterForm.querySelector('input');
        
        newsletterBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            const email = newsletterInput.value.trim();
            
            if (email && validateEmail(email)) {
                showNotification('Thank you for subscribing!', 'success');
                newsletterInput.value = '';
            } else {
                showNotification('Please enter a valid email address', 'warning');
            }
        });
    }
});

// ===========================
// Utility Functions
// ===========================

// Email validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notification if any
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background-color: ${getNotificationColor(type)};
        color: white;
        border-radius: 4px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
        font-weight: 500;
        max-width: 300px;
    `;
    
    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
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
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    
    if (!document.querySelector('style[data-notification]')) {
        style.setAttribute('data-notification', 'true');
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
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

// ===========================
// Smooth Scrolling
// ===========================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===========================
// Sticky Header on Scroll
// ===========================
let lastScroll = 0;
const header = document.querySelector('header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
        return;
    }
    
    if (currentScroll > lastScroll && currentScroll > 100) {
        // Scrolling down
        header.style.transform = 'translateY(-100%)';
    } else {
        // Scrolling up
        header.style.transform = 'translateY(0)';
        header.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    }
    
    lastScroll = currentScroll;
});

// ===========================
// Product Card Animations
// ===========================
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply fade-in animation to product cards
document.querySelectorAll('.product-card').forEach((card, index) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = `all 0.5s ease ${index * 0.1}s`;
    observer.observe(card);
});

// ===========================
// Mobile Menu Toggle (for future enhancement)
// ===========================
function toggleMobileMenu() {
    const nav = document.querySelector('.main-nav');
    nav.classList.toggle('mobile-active');
}

// ===========================
// Image Lazy Loading Fallback
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// ===========================
// Hero Button Actions
// ===========================
const heroButtons = document.querySelectorAll('.hero-buttons .btn');

heroButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (this.classList.contains('btn-primary')) {
            // Scroll to featured section
            const featuredSection = document.querySelector('.featured-section');
            if (featuredSection) {
                featuredSection.scrollIntoView({ behavior: 'smooth' });
            }
        } else if (this.classList.contains('btn-secondary')) {
            showNotification('List your items feature coming soon!', 'info');
        }
    });
});

// ===========================
// Promo Card Actions
// ===========================
const promoButtons = document.querySelectorAll('.promo-card .btn, .promo-card a');

promoButtons.forEach(button => {
    button.addEventListener('click', function(e) {
        e.preventDefault();
        showNotification('Special offers loading...', 'info');
    });
});

// ===========================
// Console Welcome Message
// ===========================
console.log('%c🏠 Welcome to RentHub! ', 'background: #b21900; color: white; font-size: 20px; padding: 10px;');
console.log('%cRent Anything, Anytime 🚀', 'color: #173641; font-size: 16px;');
