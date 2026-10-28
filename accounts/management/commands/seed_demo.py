"""
Management command to seed demo users and initial blood stock.

Usage:
    python manage.py seed_demo
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from inventory.models import BloodStock

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds initial demo users for each role and starting blood stock inventory.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting demo database seed...'))

        # 1. Create demo users for each role
        demo_users = [
            {
                'username': 'demo_donor',
                'email': 'donor@bbms.local',
                'password': 'DonorPassword123!',
                'role': 'donor',
                'blood_group': 'O+',
                'phone': '+91-9876543210',
            },
            {
                'username': 'demo_staff',
                'email': 'staff@bbms.local',
                'password': 'StaffPassword123!',
                'role': 'staff',
                'blood_group': '',
                'phone': '+91-9876543211',
            },
            {
                'username': 'demo_hospital',
                'email': 'hospital@bbms.local',
                'password': 'HospitalPassword123!',
                'role': 'hospital',
                'blood_group': '',
                'phone': '+91-9876543212',
            },
            {
                'username': 'demo_admin',
                'email': 'admin@bbms.local',
                'password': 'AdminPassword123!',
                'role': 'admin',
                'blood_group': '',
                'phone': '+91-9876543213',
                'is_staff': True,
                'is_superuser': True,
            },
        ]

        for user_data in demo_users:
            username = user_data['username']
            is_staff = user_data.pop('is_staff', False)
            is_superuser = user_data.pop('is_superuser', False)
            password = user_data.pop('password')

            user, created = User.objects.get_or_create(
                username=username,
                defaults=user_data,
            )
            user.set_password(password)
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()

            action = 'Created' if created else 'Updated'
            self.stdout.write(f"  {action} user: {username} (Role: {user.role})")

        # 2. Seed initial blood inventory for all 8 blood groups x 4 components
        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        components = ['whole_blood', 'red_cells', 'plasma', 'platelets']

        # Baseline demo stock levels (some low to demonstrate low-stock alert)
        baseline_quantities = {
            ('O+', 'whole_blood'): 15,
            ('O+', 'red_cells'): 8,
            ('O+', 'plasma'): 12,
            ('O+', 'platelets'): 3,  # Low stock
            ('A+', 'whole_blood'): 10,
            ('A+', 'red_cells'): 6,
            ('A+', 'plasma'): 7,
            ('A+', 'platelets'): 2,  # Low stock
            ('B+', 'whole_blood'): 8,
            ('B+', 'red_cells'): 5,
            ('B+', 'plasma'): 6,
            ('B+', 'platelets'): 4,
            ('AB+', 'whole_blood'): 4,
            ('AB+', 'red_cells'): 3,
            ('AB+', 'plasma'): 5,
            ('AB+', 'platelets'): 1,  # Low stock
            ('O-', 'whole_blood'): 2,  # Rare / low stock
            ('O-', 'red_cells'): 1,   # Low stock
            ('O-', 'plasma'): 3,
            ('O-', 'platelets'): 1,   # Low stock
            ('A-', 'whole_blood'): 3,
            ('A-', 'red_cells'): 2,
            ('A-', 'plasma'): 4,
            ('A-', 'platelets'): 1,
            ('B-', 'whole_blood'): 2,
            ('B-', 'red_cells'): 2,
            ('B-', 'plasma'): 3,
            ('B-', 'platelets'): 1,
            ('AB-', 'whole_blood'): 1,  # Low stock
            ('AB-', 'red_cells'): 1,
            ('AB-', 'plasma'): 2,
            ('AB-', 'platelets'): 1,
        }

        total_seeded = 0
        for bg in blood_groups:
            for comp in components:
                qty = baseline_quantities.get((bg, comp), 5)
                stock, _ = BloodStock.objects.get_or_create(
                    blood_group=bg,
                    component=comp,
                    defaults={'units_available': qty}
                )
                stock.units_available = qty
                stock.save()
                total_seeded += 1

        self.stdout.write(f"  Seeded {total_seeded} inventory records across all blood groups.")
        self.stdout.write(self.style.SUCCESS('Demo data seeding completed successfully!'))
