from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Application
from premium.models import Premium


@receiver(pre_save, sender=Application)
def create_premiums_on_approval(sender, instance, **kwargs):
    """
    Automatically create premium records when an application is approved.
    """
    # Check if this is an existing application
    if instance.pk:
        try:
            # Get the old application from database
            old_application = Application.objects.get(pk=instance.pk)
            
            # Check if status is changing from something else to 'Approved'
            if old_application.status != 'Approved' and instance.status == 'Approved':
                # Check if premiums already exist for this application
                existing_premiums = Premium.objects.filter(application=instance)
                if not existing_premiums.exists():
                    # Create premiums for the duration of the policy
                    create_premiums_for_application(instance)
                    
        except Application.DoesNotExist:
            # This is a new application, don't create premiums yet
            pass


def create_premiums_for_application(application):
    """
    Create monthly premium records for an approved application.
    """
    premium_amount = application.policy.premium_amount
    duration_months = application.policy.duration_months
    
    # Create monthly premiums starting from next month
    for month in range(duration_months):
        due_date = timezone.now() + timedelta(days=30 * (month + 1))
        
        # Set initial status - first premium is pending, others are pending
        # In a real system, you might have different logic here
        status = 'Pending'
        payment_date = None
        payment_method = None
        transaction_id = None
        
        # Create the premium record
        Premium.objects.create(
            application=application,
            amount_paid=premium_amount,
            payment_date=payment_date,
            due_date=due_date,
            status=status,
            payment_method=payment_method,
            transaction_id=transaction_id
        )
