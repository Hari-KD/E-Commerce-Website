# Nehaa Gallerina - Django E-commerce Backend

A complete Django backend for the Nehaa Gallerina gemstone e-commerce website. This project converts the static HTML/CSS/JS frontend into a fully dynamic, database-driven application.

## 🎯 Features

### Core Functionality
- **Dynamic Product Management**: All 20+ static product pages consolidated into a single dynamic template
- **User Authentication**: Login, registration, and role-based access (Admin/User)
- **Shopping Cart**: Session-based cart for guests, database cart for authenticated users
- **Checkout & Orders**: Complete order processing with Razorpay payment integration
- **Admin Dashboard**: Comprehensive analytics and management interface
- **RESTful API**: JSON endpoints for cart operations

### Apps Structure
- **store**: Product catalog, cart, orders, and checkout
- **users**: Custom user model, authentication, and profiles
- **dashboard**: Admin analytics and management views

## 📋 Requirements

- Python 3.8+
- Django 4.2.7
- SQLite (default) or PostgreSQL/MySQL
- Pillow for image handling
- See `requirements.txt` for complete list

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root (copy from `.env.example`):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Razorpay Settings
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

### 3. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create test users (admin and regular user)
python manage.py create_test_users

# Load sample products
python manage.py load_products
```

### 4. Copy Static Files

```bash
# Copy style.css to static directory
copy style.css static\style.css

# Copy cart.js to static/js directory
copy cart.js static\js\cart.js

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 👤 Test Credentials

### Admin Access
- **Username**: admin
- **Password**: admin123
- **URL**: http://127.0.0.1:8000/accounts/login/ (select "Admin" role)

### Regular User
- **Username**: user
- **Password**: user123
- **URL**: http://127.0.0.1:8000/accounts/login/ (select "User" role)

## 📁 Project Structure

```
gemstone_ecommerce/
├── gemstone_ecommerce/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                   # Store app
│   ├── models.py           # Product, Cart, Order models
│   ├── views.py            # Store views and API endpoints
│   ├── urls.py
│   ├── admin.py
│   └── management/
│       └── commands/
│           └── load_products.py
├── users/                   # Users app
│   ├── models.py           # CustomUser model
│   ├── views.py            # Auth views
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── create_test_users.py
├── dashboard/               # Admin dashboard app
│   ├── views.py            # Dashboard analytics
│   └── urls.py
├── templates/               # Django templates
│   ├── base.html
│   ├── store/
│   │   ├── index.html
│   │   ├── shop.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   └── checkout.html
│   ├── users/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── user_home.html
│   └── dashboard/
│       └── admin_dashboard.html
├── static/                  # Static files
│   ├── css/
│   ├── js/
│   └── style.css
├── media/                   # Uploaded files
├── manage.py
├── requirements.txt
└── README.md
```

## 🔑 Key Features Explained

### 1. Dynamic Product Pages
All 20+ static product HTML files have been replaced with a single dynamic template (`product_detail.html`) that fetches product data from the database using slugs.

**URL Pattern**: `/product/<slug>/`

Example:
- Old: `product1-citrine.html`
- New: `/product/citrine-faceted/`

### 2. Shopping Cart System

#### For Guest Users:
- Cart stored in session
- Cart ID generated automatically
- Persists across page reloads

#### For Authenticated Users:
- Cart stored in database
- Linked to user account
- Accessible from any device

#### API Endpoints:
- `POST /api/cart/add/<product_id>/` - Add item to cart
- `POST /api/cart/update/<item_id>/` - Update quantity
- `POST /api/cart/remove/<item_id>/` - Remove item
- `GET /api/cart/data/` - Get cart contents (JSON)

### 3. Order Processing

1. User adds items to cart
2. Proceeds to checkout
3. Fills shipping information
4. Completes payment via Razorpay
5. Order created in database
6. Stock updated automatically
7. Loyalty points awarded

### 4. Admin Dashboard

Access at: `/dashboard/`

Features:
- Total orders, sales, and revenue statistics
- Sales and revenue charts (Chart.js)
- Recent orders table
- Growth percentages
- Monthly target tracking

### 5. User Profiles

Users can:
- View order history
- Track loyalty points
- Update profile information
- View account statistics

## 🛠️ Management Commands

### Create Test Users
```bash
python manage.py create_test_users
```
Creates:
- Admin user (admin/admin123)
- Regular user (user/user123)

### Load Sample Products
```bash
python manage.py load_products
```
Loads all 20 products from the static HTML files into the database with:
- Product details
- Images (URLs)
- Pricing
- Stock levels
- Categories

### Create Superuser (Alternative)
```bash
python manage.py createsuperuser
```

## 🎨 Template Conversion

All static HTML files have been converted to Django templates with:

### Django Template Language (DTL) Features:
- `{% extends 'base.html' %}` - Template inheritance
- `{% url 'store:product_detail' product.slug %}` - Dynamic URLs
- `{% for product in products %}` - Loops
- `{% if user.is_authenticated %}` - Conditionals
- `{{ product.name }}` - Variable output
- `{% load static %}` - Static file loading

### Example Conversion:

**Before (Static HTML):**
```html
<a href="product1-citrine.html">AAA+ Citrine</a>
```

**After (Django Template):**
```html
<a href="{% url 'store:product_detail' product.slug %}">{{ product.name }}</a>
```

## 💳 Payment Integration

### Razorpay Setup

1. Sign up at [https://razorpay.com](https://razorpay.com)
2. Get API keys from dashboard
3. Update `.env` file:
   ```env
   RAZORPAY_KEY_ID=rzp_live_your_key
   RAZORPAY_KEY_SECRET=your_secret
   ```
4. Update `checkout.html` with your key

### Test Mode
Currently configured for test mode. Use test card:
- **Card**: 4111 1111 1111 1111
- **CVV**: Any 3 digits
- **Expiry**: Any future date

## 📊 Database Models

### Product Model
- name, slug, description, price
- image (URL), image_file (upload)
- stock, category
- product_type, origin, size, treatment
- is_available, is_featured

### Order Model
- user, order_number
- Customer details (name, email, phone, address)
- total_price, order_status
- payment_id, is_paid

### CustomUser Model
- Extends Django's AbstractUser
- Additional fields: phone_number, address, loyalty_points
- Methods: get_total_orders(), get_total_spent()

## 🔐 Security Notes

- CSRF protection enabled
- Password hashing (Django default)
- Session security
- SQL injection protection (ORM)
- XSS protection (template escaping)

**Production Checklist:**
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure HTTPS
- [ ] Use environment variables
- [ ] Set up proper database (PostgreSQL)
- [ ] Configure email backend
- [ ] Set up proper media storage (S3)
- [ ] Implement rate limiting
- [ ] Add logging

## 🚢 Deployment

### Prepare for Production

1. Update settings:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

2. Use PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Collect static files:
```bash
python manage.py collectstatic
```

4. Use a production server (Gunicorn):
```bash
pip install gunicorn
gunicorn gemstone_ecommerce.wsgi:application
```

## 📝 API Documentation

### Cart API

#### Add to Cart
```
POST /api/cart/add/<product_id>/
Body: quantity=1
Response: {
  "success": true,
  "message": "Product added to cart",
  "cart_count": 3
}
```

#### Update Cart Item
```
POST /api/cart/update/<item_id>/
Body: quantity=2
Response: {
  "success": true,
  "message": "Cart updated",
  "subtotal": 116.00
}
```

#### Remove from Cart
```
POST /api/cart/remove/<item_id>/
Response: {
  "success": true,
  "message": "Item removed from cart"
}
```

#### Get Cart Data
```
GET /api/cart/data/
Response: {
  "cart_items": [...],
  "total": 174.50,
  "count": 3
}
```

## 🐛 Troubleshooting

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Database errors
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: Admin can't login
```bash
python manage.py createsuperuser
```

### Issue: Products not showing
```bash
python manage.py load_products
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Razorpay Documentation](https://razorpay.com/docs/)

## 🤝 Contributing

This is a complete backend implementation for the Nehaa Gallerina e-commerce site. Feel free to extend it with additional features.

## 📄 License

This project is for educational purposes.

## ✨ Features to Add (Future)

- [ ] Product reviews and ratings
- [ ] Wishlist functionality
- [ ] Email notifications
- [ ] Invoice generation (PDF)
- [ ] Inventory alerts
- [ ] Coupon/discount system
- [ ] Multi-currency support
- [ ] Advanced search and filters
- [ ] Product recommendations
- [ ] Social media integration

---

**Built with Django 4.2.7 | Python 3.8+**
