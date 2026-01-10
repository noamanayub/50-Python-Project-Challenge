from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem, Review, Wishlist, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'owner', 'daily_rate', 'is_available', 'rating', 'created_at']
    list_filter = ['category', 'is_available', 'condition', 'created_at']
    search_fields = ['title', 'description', 'owner__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]
    readonly_fields = ['views', 'rating', 'total_reviews', 'created_at', 'updated_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'renter', 'status', 'total', 'start_date', 'end_date', 'created_at']
    list_filter = ['status', 'delivery_method', 'created_at']
    search_fields = ['order_number', 'renter__username', 'email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'verified_rental', 'created_at']
    list_filter = ['rating', 'verified_rental', 'created_at']
    search_fields = ['user__username', 'product__title', 'title', 'comment']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'is_verified', 'rating', 'total_rentals', 'total_listings']
    list_filter = ['is_verified', 'id_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['total_rentals', 'total_listings', 'rating', 'created_at']
