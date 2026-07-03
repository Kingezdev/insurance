from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from policies.models import Application
from premium.models import Premium


class Command(BaseCommand):
    help = 'Create premium records for approved applications'

    def handle(self, *args, **options):
        self.stdout.write('Creating premium records for approved applications...')
        
        # Get all approved applications
        approved_applications = Application.objects.filter(status='Approved')
        
        if not approved_applications.exists():
            self.stdout.write('No approved applications found.')
            return
        
        created_count = 0
        
        for application in approved_applications:
            # Check if premiums already exist for this application
            existing_premiums = Premium.objects.filter(application=application)
            if existing_premiums.exists():
                self.stdout.write(f'Skipping application {application.id} - premiums already exist')
                continue
            
            # Create premiums for the duration of the policy
            premium_amount = application.policy.premium_amount
            duration_months = application.policy.duration_months
            
            # Create monthly premiums
            for month in range(duration_months):
                due_date = timezone.now() + timedelta(days=30 * (month + 1))
                
                # Create premium with different statuses for testing
                if month == 0:
                    # First premium - paid
                    payment_date = due_date - timedelta(days=5)
                    status = 'Paid'
                    payment_method = 'Credit Card'
                    transaction_id = f'TXN{application.id}{month:02d}'
                elif month == 1:
                    # Second premium - paid
                    payment_date = due_date - timedelta(days=2)
                    status = 'Paid'
                    payment_method = 'Bank Transfer'
                    transaction_id = f'TXN{application.id}{month:02d}'
                elif month == 2:
                    # Third premium - pending
                    payment_date = None
                    status = 'Pending'
                    payment_method = None
                    transaction_id = None
                elif month == 3:
                    # Fourth premium - overdue
                    payment_date = None
                    status = 'Overdue'
                    payment_method = None
                    transaction_id = None
                else:
                    # Future premiums - pending
                    payment_date = None
                    status = 'Pending'
                    payment_method = None
                    transaction_id = None
                
                premium = Premium.objects.create(
                    application=application,
                    amount_paid=premium_amount,
                    payment_date=payment_date,
                    due_date=due_date,
                    status=status,
                    payment_method=payment_method,
                    transaction_id=transaction_id
                )
                
                created_count += 1
                self.stdout.write(
                    f'Created premium for application {application.id} - '
                    f'{application.policy.name} - {status} - Due: {due_date.strftime("%Y-%m-%d")}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} premium records '
                f'for {approved_applications.count()} approved applications'
            )
        )
