from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Create test users (admin and regular user)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test users...')
        
        # Create admin user
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin',
                email='admin@nehaagallerina.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: admin / admin123'))
        else:
            self.stdout.write('Admin user already exists')
        
        # Create regular user
        if not CustomUser.objects.filter(username='user').exists():
            user = CustomUser.objects.create_user(
                username='user',
                email='user@nehaagallerina.com',
                password='user123',
                first_name='Test',
                last_name='User',
                phone_number='1234567890',
                address='123 Test Street',
                city='Mumbai',
                state='Maharashtra',
                pincode='400001',
                loyalty_points=450
            )
            self.stdout.write(self.style.SUCCESS('Created regular user: user / user123'))
        else:
            self.stdout.write('Regular user already exists')
        
        self.stdout.write(self.style.SUCCESS('\nTest users created successfully!'))
        self.stdout.write('Login credentials:')
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  User: user / user123')
