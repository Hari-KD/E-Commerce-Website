from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from store.models import Order, Product, OrderItem
from users.models import CustomUser


@login_required
@staff_member_required
def admin_dashboard_view(request):
    """
    Admin dashboard view - displays statistics and analytics.
    Powers the admin-dashboard.html template.
    """
    # Calculate date ranges
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    
    # Total orders
    total_orders = Order.objects.count()
    orders_this_month = Order.objects.filter(created_at__gte=last_month).count()
    
    # Total sales (sum of all completed orders)
    total_sales = Order.objects.filter(
        order_status__in=['Completed', 'Shipped', 'Delivered']
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    sales_this_month = Order.objects.filter(
        created_at__gte=last_month,
        order_status__in=['Completed', 'Shipped', 'Delivered']
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Revenue (same as sales for now)
    revenue = total_sales
    revenue_this_month = sales_this_month
    
    # Monthly target (hardcoded for now, can be made dynamic)
    monthly_target = 50000
    target_completion = (sales_this_month / monthly_target * 100) if monthly_target > 0 else 0
    
    # Total users
    total_users = CustomUser.objects.count()
    new_users_this_month = CustomUser.objects.filter(date_joined__gte=last_month).count()
    
    # Total products
    total_products = Product.objects.count()
    available_products = Product.objects.filter(is_available=True).count()
    
    # Recent orders (last 10)
    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:10]
    
    # Sales data for chart (last 6 months)
    sales_data = []
    revenue_data = []
    labels = []
    
    for i in range(5, -1, -1):
        month_start = today - timedelta(days=30*i)
        month_end = today - timedelta(days=30*(i-1)) if i > 0 else today
        
        month_sales = Order.objects.filter(
            created_at__gte=month_start,
            created_at__lt=month_end,
            order_status__in=['Completed', 'Shipped', 'Delivered']
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        sales_data.append(float(month_sales))
        revenue_data.append(float(month_sales * 0.7))  # Assuming 70% is revenue
        labels.append(month_start.strftime('%b'))
    
    # Order status breakdown
    order_status_counts = Order.objects.values('order_status').annotate(count=Count('id'))
    
    # Top selling products
    top_products = Product.objects.annotate(
        total_sold=Count('orderitem')
    ).order_by('-total_sold')[:5]
    
    # Calculate growth percentages
    if orders_this_month > 0 and total_orders > orders_this_month:
        orders_growth = ((orders_this_month / (total_orders - orders_this_month)) * 100)
    else:
        orders_growth = 0
    
    if sales_this_month > 0 and total_sales > sales_this_month:
        sales_growth = ((sales_this_month / (total_sales - sales_this_month)) * 100)
    else:
        sales_growth = 0
    
    context = {
        'total_orders': total_orders,
        'orders_this_month': orders_this_month,
        'orders_growth': round(orders_growth, 1),
        
        'total_sales': total_sales,
        'sales_this_month': sales_this_month,
        'sales_growth': round(sales_growth, 1),
        
        'revenue': revenue,
        'revenue_this_month': revenue_this_month,
        
        'monthly_target': monthly_target,
        'target_completion': round(target_completion, 1),
        
        'total_users': total_users,
        'new_users_this_month': new_users_this_month,
        
        'total_products': total_products,
        'available_products': available_products,
        
        'recent_orders': recent_orders,
        
        # Chart data
        'sales_data': sales_data,
        'revenue_data': revenue_data,
        'chart_labels': labels,
        
        'order_status_counts': list(order_status_counts),
        'top_products': top_products,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@staff_member_required
def manage_products_view(request):
    """
    Product management view for admin.
    """
    products = Product.objects.all().order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, 'dashboard/manage_products.html', context)


@login_required
@staff_member_required
def manage_orders_view(request):
    """
    Order management view for admin.
    """
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(order_status=status)
    
    context = {
        'orders': orders,
        'selected_status': status,
    }
    return render(request, 'dashboard/manage_orders.html', context)


@login_required
@staff_member_required
def manage_users_view(request):
    """
    User management view for admin.
    """
    users = CustomUser.objects.all().order_by('-date_joined')
    
    context = {
        'users': users,
    }
    return render(request, 'dashboard/manage_users.html', context)
