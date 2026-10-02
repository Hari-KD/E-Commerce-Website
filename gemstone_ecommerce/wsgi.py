"""
WSGI config for gemstone_ecommerce project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gemstone_ecommerce.settings')

application = get_wsgi_application()

# Auto-migrate database on Vercel serverless environment
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False, verbosity=0)
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(is_staff=True).exists():
        call_command('create_test_users', interactive=False, verbosity=0)
        call_command('load_products', interactive=False, verbosity=0)
except Exception as e:
    print(f"Vercel DB Init Notice: {e}")

app = application
