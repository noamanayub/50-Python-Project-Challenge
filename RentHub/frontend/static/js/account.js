function showSection(sectionId) {
    event.preventDefault();
    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    event.target.classList.add('active');
}

function logout() {
    event.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/logout/';
    }
}

// Profile form is now handled by Django, no need to prevent default
