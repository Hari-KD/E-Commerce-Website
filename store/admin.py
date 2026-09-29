from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin configuration.
    """
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin configuration.
    """
    list_display = ['name', 'category', 'price', 'stock', 'is_available', 'is_featured', 'created_at']
    list_filter = ['category', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'product_type', 'origin']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available', 'is_featured']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'price', 'stock')
        }),
        ('Images', {
            'fields': ('image', 'image_file')
        }),
        ('Specifications', {
            'fields': ('product_type', 'origin', 'size', 'treatment')
        }),
        ('Status', {
            'fields': ('is_available', 'is_featured')
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Cart admin configuration.
    """
    list_display = ['cart_id', 'date_added']
    search_fields = ['cart_id']
    ordering = ['-date_added']


class CartItemInline(admin.TabularInline):
    """
    Inline admin for cart items.
    """
    model = CartItem
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Cart Item admin configuration.
    """
    list_display = ['get_user_or_cart', 'product', 'quantity', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['product__name', 'user__username']
    ordering = ['-created_at']
    
    def get_user_or_cart(self, obj):
        if obj.user:
            return f"User: {obj.user.username}"
        return f"Cart: {obj.cart.cart_id[:10]}..."
    get_user_or_cart.short_description = 'Owner'


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Order admin configuration.
    """
    list_display = ['order_number', 'get_customer_name', 'user', 'total_price', 
                   'order_status', 'is_paid', 'created_at']
    list_filter = ['order_status', 'is_paid', 'created_at']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone']
    list_editable = ['order_status']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'order_status', 'total_price')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 
                      'address', 'city', 'state', 'pincode', 'country')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_id', 'is_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Order Item admin configuration.
    """
    list_display = ['order', 'product', 'quantity', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product__name']
    ordering = ['-created_at']
