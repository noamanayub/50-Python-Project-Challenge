from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('search/', views.search, name='search'),
    
    # User pages
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    
    # Cart and Checkout
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    # Wishlist
    path('wishlist/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    
    # Other pages
    path('featured/', views.featured_view, name='featured'),
    path('best-deals/', views.best_deals_view, name='best-deals'),
    path('new-arrivals/', views.new_arrivals_view, name='new-arrivals'),
    path('list-item/', views.list_item_view, name='list-item'),
    path('how-it-works/', views.how_it_works_view, name='how-it-works'),
    path('about/', views.about_view, name='about'),
    path('help/', views.help_view, name='help'),
    path('safety/', views.safety_view, name='safety'),
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('contact/', views.contact_view, name='contact'),
    path('blog/', views.blog_view, name='blog'),
]
