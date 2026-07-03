from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from policies.models import Policy, Application


class Command(BaseCommand):
    help = 'Create seed data for applications with different statuses'

    def handle(self, *args, **options):
        self.stdout.write('Creating seed data for applications...')
        
        # Get or create a test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('Created test user: testuser')
        
        # Create policies if they don't exist
        policies_data = [
            {
                'name': 'Premium Life Insurance',
                'type': 'Life',
                'premium_amount': 250.00,
                'coverage_amount': 500000.00,
                'duration_months': 12,
                'description': 'Comprehensive life insurance coverage with death benefits and investment options.'
            },
            {
                'name': 'Motor Vehicle Insurance',
                'type': 'Motor',
                'premium_amount': 150.00,
                'coverage_amount': 25000.00,
                'duration_months': 6,
                'description': 'Complete motor vehicle insurance covering accidents, theft, and third-party liability.'
            },
            {
                'name': 'Health Plus Insurance',
                'type': 'Health',
                'premium_amount': 300.00,
                'coverage_amount': 100000.00,
                'duration_months': 12,
                'description': 'Comprehensive health insurance covering medical expenses, hospitalization, and treatments.'
            },
            {
                'name': 'Basic Life Coverage',
                'type': 'Life',
                'premium_amount': 100.00,
                'coverage_amount': 100000.00,
                'duration_months': 12,
                'description': 'Basic life insurance with essential death benefit coverage.'
            },
            {
                'name': 'Family Health Plan',
                'type': 'Health',
                'premium_amount': 450.00,
                'coverage_amount': 200000.00,
                'duration_months': 12,
                'description': 'Family health insurance covering all family members with comprehensive medical benefits.'
            }
        ]
        
        policies = []
        for policy_data in policies_data:
            policy, created = Policy.objects.get_or_create(
                name=policy_data['name'],
                defaults=policy_data
            )
            if created:
                self.stdout.write(f'Created policy: {policy.name}')
            policies.append(policy)
        
        # Delete existing applications for clean seed
        Application.objects.filter(client=test_user).delete()
        self.stdout.write('Cleared existing applications for test user')
        
        # Create applications with different statuses
        applications_data = [
            # Approved applications
            {
                'policy': policies[0],  # Premium Life Insurance
                'status': 'Approved',
                'applied_date': timezone.now() - timedelta(days=30),
                'approved_date': timezone.now() - timedelta(days=25),
                'notes': 'Application approved after medical examination. All documents verified.'
            },
            {
                'policy': policies[1],  # Motor Vehicle Insurance
                'status': 'Approved',
                'applied_date': timezone.now() - timedelta(days=20),
                'approved_date': timezone.now() - timedelta(days=15),
                'notes': 'Vehicle inspection completed. Policy approved with standard terms.'
            },
            {
                'policy': policies[2],  # Health Plus Insurance
                'status': 'Approved',
                'applied_date': timezone.now() - timedelta(days=10),
                'approved_date': timezone.now() - timedelta(days=5),
                'notes': 'Health check-up completed. Policy approved with family coverage.'
            },
            
            # Rejected applications
            {
                'policy': policies[3],  # Basic Life Coverage
                'status': 'Rejected',
                'applied_date': timezone.now() - timedelta(days=35),
                'rejected_date': timezone.now() - timedelta(days=30),
                'notes': 'Application rejected due to pre-existing medical conditions. Please consult with our medical team.'
            },
            {
                'policy': policies[4],  # Family Health Plan
                'status': 'Rejected',
                'applied_date': timezone.now() - timedelta(days=25),
                'rejected_date': timezone.now() - timedelta(days=20),
                'notes': 'Application rejected due to incomplete documentation. Please resubmit with all required forms.'
            },
            
            # Pending applications
            {
                'policy': policies[0],  # Premium Life Insurance
                'status': 'Pending',
                'applied_date': timezone.now() - timedelta(days=5),
                'notes': 'Application under review. Medical examination scheduled for next week.'
            },
            {
                'policy': policies[2],  # Health Plus Insurance
                'status': 'Pending',
                'applied_date': timezone.now() - timedelta(days=3),
                'notes': 'Application under review. Additional documentation requested.'
            },
            {
                'policy': policies[1],  # Motor Vehicle Insurance
                'status': 'Pending',
                'applied_date': timezone.now() - timedelta(days=1),
                'notes': 'Application received. Vehicle inspection pending.'
            }
        ]
        
        created_count = 0
        for app_data in applications_data:
            application = Application.objects.create(
                client=test_user,
                **app_data
            )
            created_count += 1
            self.stdout.write(
                f'Created {application.status} application: {application.policy.name} '
                f'(Applied: {application.applied_date.strftime("%Y-%m-%d")})'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} seed applications '
                f'({len([a for a in applications_data if a["status"] == "Approved"])} approved, '
                f'{len([a for a in applications_data if a["status"] == "Rejected"])} rejected, '
                f'{len([a for a in applications_data if a["status"] == "Pending"])} pending)'
            )
        )
