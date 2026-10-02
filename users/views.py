from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from store.models import Order


def login_view(request):
    """
    User login view with role auto-detection.
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:admin_dashboard')
        return redirect('users:user_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check role if specifically requested
            if role == 'admin' and not user.is_staff:
                messages.error(request, 'Invalid credentials for admin access')
                return render(request, 'users/login.html')
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on staff status
            if user.is_staff:
                return redirect('dashboard:admin_dashboard')
            return redirect('users:user_home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')


def register_view(request):
    """
    User registration view - creates user in database and logs them in.
    """
    if request.user.is_authenticated:
        return redirect('users:user_home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        
        # Validation
        if not username or not email or not password:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'users/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'users/register.html')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'users/register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email address is already registered.')
            return render(request, 'users/register.html')
        
        # Create user in database
        try:
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Log in the user automatically
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome to Nehaa Gallerina, {user.username}!')
            return redirect('users:user_home')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'users/register.html')
    
    return render(request, 'users/register.html')


def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('store:home')


@login_required
def user_home_view(request):
    """
    User home/profile page view.
    Displays user statistics and recent orders.
    """
    user = request.user
    
    # Get user orders
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Calculate statistics
    total_orders = Order.objects.filter(user=user).count()
    total_spent = user.get_total_spent()
    
    # Count total products purchased
    from store.models import OrderItem
    total_products = OrderItem.objects.filter(order__user=user).count()
    
    context = {
        'user': user,
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'total_products': total_products,
        'loyalty_points': user.loyalty_points,
    }
    return render(request, 'users/user_home.html', context)


@login_required
def profile_view(request):
    """
    User profile edit view.
    """
    if request.method == 'POST':
        user = request.user
        
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.address = request.POST.get('address', '')
        user.city = request.POST.get('city', '')
        user.state = request.POST.get('state', '')
        user.pincode = request.POST.get('pincode', '')
        user.country = request.POST.get('country', 'India')
        
        user.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('users:profile')
    
    return render(request, 'users/profile.html')


@login_required
def order_history_view(request):
    """
    User order history view.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'users/order_history.html', context)


@login_required
def order_detail_view(request, order_number):
    """
    Order detail view.
    """
    order = Order.objects.get(order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'users/order_detail.html', context)
