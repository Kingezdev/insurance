from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Premium
from policies.models import Application


@login_required
def premium_history_view(request):
    """Display premium payment history with payment dates, amounts, next due date"""
    premiums = Premium.objects.filter(
        application__client=request.user
    ).order_by('-due_date')
    
    # Calculate statistics
    total_paid = premiums.filter(status='Paid').count()
    total_amount_paid = sum(p.amount_paid for p in premiums.filter(status='Paid'))
    pending_count = premiums.filter(status='Pending').count()
    overdue_count = premiums.filter(status='Overdue').count()
    
    # Get next due premium
    next_due = premiums.filter(status='Pending').order_by('due_date').first()
    
    context = {
        'premiums': premiums,
        'stats': {
            'total_paid': total_paid,
            'total_amount_paid': total_amount_paid,
            'pending_count': pending_count,
            'overdue_count': overdue_count,
        },
        'next_due': next_due,
    }
    return render(request, 'premium/premium_history.html', context)


@login_required
def premium_detail_view(request, premium_id):
    """Show detailed view of a specific premium"""
    premium = get_object_or_404(
        Premium, 
        id=premium_id, 
        application__client=request.user
    )
    
    context = {
        'premium': premium,
    }
    return render(request, 'premium/premium_detail.html', context)
