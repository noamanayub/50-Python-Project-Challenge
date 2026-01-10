// ===========================
// Toggle Password Visibility
// ===========================
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.toggle-password');
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// ===========================
// Switch Between Forms
// ===========================
function switchToRegister(e) {
    e.preventDefault();
    document.getElementById('signInBox').style.display = 'none';
    document.getElementById('registerBox').style.display = 'block';
}

function switchToSignIn(e) {
    e.preventDefault();
    document.getElementById('registerBox').style.display = 'none';
    document.getElementById('signInBox').style.display = 'block';
}

// ===========================
// Form Validation
// ===========================
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    // At least 8 characters, one letter and one number
    const re = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$/;
    return re.test(password);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

// ===========================
// Sign In Form Handler
// ===========================
document.getElementById('signInForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('signInEmail').value.trim();
    const password = document.getElementById('signInPassword').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    // Validation
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    if (password.length < 6) {
        showNotification('Password is too short', 'error');
        return;
    }
    
    // Simulate login
    showNotification('Signing in...', 'info');
    
    setTimeout(() => {
        // Store user info
        const userData = {
            email: email,
            loggedIn: true,
            timestamp: new Date().toISOString()
        };
        
        if (rememberMe) {
            localStorage.setItem('renthub_user', JSON.stringify(userData));
        } else {
            sessionStorage.setItem('renthub_user', JSON.stringify(userData));
        }
        
        showNotification('Sign in successful! Redirecting...', 'success');
        
        setTimeout(() => {
            window.location.href = '../../index.html';
        }, 1500);
    }, 1000);
});

// ===========================
// Register Form Handler
// ===========================
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const phone = document.getElementById('registerPhone').value.trim();
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const termsAgree = document.getElementById('termsAgree').checked;
    
    // Validation
    if (!firstName || !lastName) {
        showNotification('Please enter your full name', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    if (!validatePhone(phone)) {
        showNotification('Please enter a valid phone number', 'error');
        return;
    }
    
    if (!validatePassword(password)) {
        showNotification('Password must be at least 8 characters with letters and numbers', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }
    
    if (!termsAgree) {
        showNotification('Please agree to the Terms of Service', 'error');
        return;
    }
    
    // Simulate registration
    showNotification('Creating your account...', 'info');
    
    setTimeout(() => {
        const userData = {
            firstName: firstName,
            lastName: lastName,
            email: email,
            phone: phone,
            loggedIn: true,
            timestamp: new Date().toISOString()
        };
        
        localStorage.setItem('renthub_user', JSON.stringify(userData));
        
        showNotification('Account created successfully! Redirecting...', 'success');
        
        setTimeout(() => {
            window.location.href = '../../index.html';
        }, 1500);
    }, 1500);
});

// ===========================
// Social Login Handlers
// ===========================
document.querySelectorAll('.btn-social').forEach(button => {
    button.addEventListener('click', function() {
        const provider = this.classList.contains('btn-google') ? 'Google' : 'Facebook';
        showNotification(`${provider} sign in coming soon!`, 'info');
    });
});

// ===========================
// Notification System
// ===========================
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
// Check if already logged in
// ===========================
window.addEventListener('DOMContentLoaded', function() {
    const userData = localStorage.getItem('renthub_user') || sessionStorage.getItem('renthub_user');
    
    if (userData) {
        const user = JSON.parse(userData);
        if (user.loggedIn) {
            showNotification('You are already logged in. Redirecting...', 'info');
            setTimeout(() => {
                window.location.href = '../../index.html';
            }, 1500);
        }
    }
});
