"""
Context processors for the core app
"""
from .models import Wishlist


def user_data(request):
    """
    Add user-specific data to all templates
    """
    context = {}
    
    if request.user.is_authenticated:
        # Get wishlist count for current user only
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        context['wishlist_count'] = wishlist_count
        
        # Cart count (using session for now)
        cart_count = request.session.get('cart_count', 0)
        context['cart_count'] = cart_count
    else:
        context['wishlist_count'] = 0
        context['cart_count'] = 0
    
    return context
