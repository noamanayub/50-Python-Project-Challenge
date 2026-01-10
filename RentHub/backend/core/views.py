from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category, Order, OrderItem, Review, Wishlist, UserProfile
import random
import string


def home(request):
    """Homepage view"""
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(is_available=True).order_by('-rating')[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context)


def product_detail(request, slug):
    """Product detail view"""
    product = get_object_or_404(Product, slug=slug)
    
    # Increment view count
    product.views += 1
    product.save(update_fields=['views'])
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    # Get reviews
    reviews = product.reviews.all()[:10]
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'product-detail/product.html', context)


def category_view(request, slug):
    """Category page view"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('daily_rate')
    elif sort_by == 'price_high':
        products = products.order_by('-daily_rate')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category.html', context)


def search(request):
    """Search view"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_available=True)
    
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'search.html', context)


@login_required
def cart_view(request):
    """Cart view"""
    return render(request, 'cart/cart.html')


@login_required
def checkout_view(request):
    """Checkout view - Creates order for current user only"""
    if request.method == 'POST':
        # Process order for current logged-in user
        order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        try:
            order = Order.objects.create(
                renter=request.user,  # Ensures order belongs to current user
                order_number=order_number,
                email=request.POST.get('email', request.user.email),
                phone=request.POST.get('phone', ''),
                delivery_method=request.POST.get('delivery_method', 'standard'),
                delivery_address=request.POST.get('address', ''),
                city=request.POST.get('city', ''),
                postal_code=request.POST.get('postal_code', ''),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                subtotal=request.POST.get('subtotal', 0),
                delivery_fee=request.POST.get('delivery_fee', 0),
                tax=request.POST.get('tax', 0),
                total=request.POST.get('total', 0),
                status='pending'
            )
            
            messages.success(request, f'Order {order_number} placed successfully!')
            return redirect('account')
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
    
    # Pre-fill user data
    user_profile = UserProfile.objects.filter(user=request.user).first()
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
def account_view(request):
    """Account dashboard view - Shows only user's own data"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get only current user's orders (all orders for stats)
    all_orders = Order.objects.filter(renter=request.user).order_by('-created_at')
    
    # Get only current user's wishlist
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    
    # Get only current user's products (items they're renting out)
    user_products = Product.objects.filter(owner=request.user)
    
    # Get only current user's reviews
    user_reviews = Review.objects.filter(user=request.user).select_related('product')[:5]
    
    # Handle profile update
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Update profile info
        user_profile.phone = request.POST.get('phone', user_profile.phone)
        user_profile.address = request.POST.get('address', user_profile.address)
        user_profile.city = request.POST.get('city', user_profile.city)
        user_profile.postal_code = request.POST.get('postal_code', user_profile.postal_code)
        user_profile.bio = request.POST.get('bio', user_profile.bio)
        user_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('account')
    
    # Calculate statistics for current user only (before slicing)
    total_orders = all_orders.count()
    total_spent = sum(order.total for order in all_orders)
    active_rentals = all_orders.filter(status='active').count()
    
    # Now slice for display
    orders = all_orders[:10]
    
    context = {
        'profile': user_profile,
        'orders': orders,
        'wishlist_items': wishlist_items,
        'user_products': user_products,
        'user_reviews': user_reviews,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'active_rentals': active_rentals,
    }
    return render(request, 'account/account.html', context)


def register_view(request):
    """Registration and login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'register':
            first_name = request.POST.get('firstName', '')
            last_name = request.POST.get('lastName', '')
            email = request.POST.get('registerEmail', '')
            phone = request.POST.get('registerPhone', '')
            password = request.POST.get('registerPassword', '')
            confirm_password = request.POST.get('confirmPassword', '')
            
            # Validation
            if not all([first_name, last_name, email, password]):
                messages.error(request, 'All fields are required.')
            elif password != confirm_password:
                messages.error(request, 'Passwords do not match.')
            elif len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
            else:
                # Create username from email
                username = email.split('@')[0]
                # Make username unique if already exists
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                UserProfile.objects.create(user=user, phone=phone)
                login(request, user)
                messages.success(request, f'Welcome {first_name}! Your account has been created successfully.')
                return redirect('home')
        
        elif action == 'login':
            email = request.POST.get('signInEmail', '')
            password = request.POST.get('signInPassword', '')
            
            # Try to find user by email
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect(request.GET.get('next', 'home'))
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    
    return render(request, 'register/register.html')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def wishlist_toggle(request, product_id):
    """Toggle wishlist item - Only affects current user's wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create wishlist item for current user only
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,  # Ensures it's the current user's wishlist
        product=product
    )
    
    if not created:
        wishlist_item.delete()
        messages.success(request, f'{product.title} removed from your wishlist.')
    else:
        messages.success(request, f'{product.title} added to your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Placeholder views for footer links
def featured_view(request):
    products = Product.objects.filter(is_available=True).order_by('-rating')
    return render(request, 'index.html', {'featured_products': products})

def best_deals_view(request):
    products = Product.objects.filter(is_available=True).order_by('daily_rate')
    return render(request, 'index.html', {'featured_products': products})

def new_arrivals_view(request):
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'index.html', {'featured_products': products})

def list_item_view(request):
    return render(request, 'list-item.html')

def how_it_works_view(request):
    return render(request, 'how-it-works.html')

def about_view(request):
    return render(request, 'about.html')

def help_view(request):
    return render(request, 'help.html')

def safety_view(request):
    return render(request, 'safety.html')

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def contact_view(request):
    return render(request, 'contact.html')

def blog_view(request):
    return render(request, 'blog.html')
