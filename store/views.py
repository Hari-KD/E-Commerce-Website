from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product, Category, Cart, CartItem, Order, OrderItem
import json
from decimal import Decimal
import uuid


def _get_cart_id(request):
    """Get or create cart ID from session."""
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart_id = str(uuid.uuid4())
        request.session['cart_id'] = cart_id
    return cart_id


def home(request):
    """
    Home page view - displays featured products with fallback to any available products.
    """
    featured_products = Product.objects.filter(
        is_featured=True, 
        is_available=True
    )[:4]
    
    if not featured_products.exists():
        featured_products = Product.objects.filter(is_available=True)[:4]
    
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'store/index.html', context)


def shop(request):
    """
    Shop page view - displays all available products.
    Supports filtering by category and search.
    """
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_active=True)
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'store/shop.html', context)


def product_detail(request, slug):
    """
    Product detail page view - displays single product.
    This replaces all 20+ static product pages.
    """
    product = get_object_or_404(Product, slug=slug, is_available=True)
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def category_products(request, slug):
    """
    Category products view - displays products in a specific category.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_available=True)
    
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'store/category_products.html', context)


def cart_view(request):
    """
    Shopping cart view - displays cart items and total.
    """
    cart_items = []
    total = Decimal('0.00')
    
    if request.user.is_authenticated:
        # Get cart items for authenticated user
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        # Get cart items for guest user
        cart_id = _get_cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except Cart.DoesNotExist:
            pass
    
    # Calculate total
    for item in cart_items:
        total += item.sub_total()
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """
    Add product to cart - API endpoint.
    """
    try:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)
        
        if product.stock < quantity:
            return JsonResponse({'error': 'Insufficient stock'}, status=400)
        
        if request.user.is_authenticated:
            # Add to user's cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                is_active=True,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Add to guest cart
            cart_id = _get_cart_id(request)
            cart, _ = Cart.objects.get_or_create(cart_id=cart_id)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                is_active=True,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        
        # Get cart count
        if request.user.is_authenticated:
            cart_count = CartItem.objects.filter(user=request.user, is_active=True).count()
        else:
            cart_count = CartItem.objects.filter(cart=cart, is_active=True).count()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': cart_count
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def update_cart(request, item_id):
    """
    Update cart item quantity - API endpoint.
    """
    try:
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        else:
            cart_id = _get_cart_id(request)
            cart = get_object_or_404(Cart, cart_id=cart_id)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity < 1:
            cart_item.delete()
            return JsonResponse({'success': True, 'message': 'Item removed from cart'})
        
        if cart_item.product.stock < quantity:
            return JsonResponse({'error': 'Insufficient stock'}, status=400)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Cart updated',
            'subtotal': float(cart_item.sub_total())
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def remove_from_cart(request, item_id):
    """
    Remove item from cart - API endpoint.
    """
    try:
        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        else:
            cart_id = _get_cart_id(request)
            cart = get_object_or_404(Cart, cart_id=cart_id)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_cart_data(request):
    """
    Get cart data as JSON - API endpoint.
    """
    cart_items = []
    total = Decimal('0.00')
    
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart_id = _get_cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            items = CartItem.objects.filter(cart=cart, is_active=True)
        except Cart.DoesNotExist:
            items = []
    
    for item in items:
        cart_items.append({
            'id': item.id,
            'product_id': item.product.id,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image': item.product.get_image_url(),
            'subtotal': float(item.sub_total())
        })
        total += item.sub_total()
    
    return JsonResponse({
        'cart_items': cart_items,
        'total': float(total),
        'count': len(cart_items)
    })


def checkout_view(request):
    """
    Checkout page view - displays order form and summary.
    """
    if request.method == 'POST':
        # Process checkout
        try:
            # Get cart items
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
                user = request.user
            else:
                cart_id = _get_cart_id(request)
                try:
                    cart = Cart.objects.get(cart_id=cart_id)
                    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                except Cart.DoesNotExist:
                    cart_items = []
                user = None
            
            if not cart_items:
                messages.error(request, 'Your cart is empty')
                return redirect('store:cart')
            
            # Calculate total
            total = sum(item.sub_total() for item in cart_items)
            
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            order = Order.objects.create(
                user=user if user else None,
                order_number=order_number,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                pincode=request.POST.get('pincode'),
                country=request.POST.get('country', 'India'),
                total_price=total,
                payment_id=request.POST.get('payment_id', ''),
                is_paid=True if request.POST.get('payment_id') else False,
                order_status='Processing' if request.POST.get('payment_id') else 'Pending',
            )
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Update stock
                product = cart_item.product
                product.stock -= cart_item.quantity
                product.save()
            
            # Clear cart
            cart_items.delete()
            
            # Add loyalty points for authenticated users
            if user:
                user.loyalty_points += int(total / 10)  # 1 point per $10
                user.save()
            
            messages.success(request, f'Order {order_number} placed successfully!')
            return redirect('store:order_success', order_number=order.order_number)
        
        except Exception as e:
            messages.error(request, f'Error processing order: {str(e)}')
            return redirect('store:checkout')
    
    # GET request - show checkout form
    cart_items = []
    total = Decimal('0.00')
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    else:
        cart_id = _get_cart_id(request)
        try:
            cart = Cart.objects.get(cart_id=cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        except Cart.DoesNotExist:
            pass
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty')
        return redirect('store:cart')
    
    for item in cart_items:
        total += item.sub_total()
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_number):
    """
    Order success page - displays order confirmation.
    """
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    return render(request, 'store/order_success.html', context)


# Static pages
def about(request):
    """About page view."""
    return render(request, 'store/about.html')


def contact(request):
    """Contact page view."""
    return render(request, 'store/contact.html')


def gemstones(request):
    """Gemstones info page view."""
    return render(request, 'store/gemstones.html')
